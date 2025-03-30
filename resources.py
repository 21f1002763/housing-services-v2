from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
from utils.decorators import *


# Login parser
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help="Username is required")
login_parser.add_argument('password', type=str, required=True, help="Password is required")

# User parser
user_parser = reqparse.RequestParser()
customer_parser = reqparse.RequestParser()
professional_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help="Username is required")
user_parser.add_argument('password', type=str, required=True, help="Password is required")
customer_parser.add_argument('user_id', type=int, required=True, help="User id is not acquired")
customer_parser.add_argument('email', type=str, required=True, help="Email is required")
customer_parser.add_argument('name', type=str, required=True, help="Name is required")
customer_parser.add_argument('mobile_no', type=int, required=True, help="Mobile number is required")
customer_parser.add_argument('address', type=str, required=False)
customer_parser.add_argument('pincode', type=int, required=False)
customer_parser.add_argument('city_id', type=int, required=True, help="Please provide city!")
user_parser.add_argument('role_name', type=str, required=True, help="Role name is required")
professional_parser.add_argument('user_id', type=int, required=True, help="User id is not acquired")
professional_parser.add_argument('email', type=str, required=True, help="Email is required")
professional_parser.add_argument('name', type=str, required=True, help="Name is required")
professional_parser.add_argument('mobile_no', type=int, required=True, help="Mobile number is required")
professional_parser.add_argument('address', type=str, required=False)
professional_parser.add_argument('pincode', type=int, required=False)
professional_parser.add_argument('city_id', type=int, required=True, help="Please provide city!")
professional_parser.add_argument('experience', type=int, required=True, help="Please provide experience!")
professional_parser.add_argument('service_id', type=int, required=True, help="Please provide service!")

# Role parser
role_parser = reqparse.RequestParser()
role_parser.add_argument('role_name', type=str, required=True, help="Role name is required")

# Service parser
service_parser = reqparse.RequestParser()
service_parser.add_argument('service_name', type=str, required=True, help="Service name is required")
service_parser.add_argument('time_required', type=int, required=True, help="Time required is required")
service_parser.add_argument('description', type=str, required=False)

# Service Package parser
service_package_parser = reqparse.RequestParser()
service_package_parser.add_argument('service_id', type=int, required=True, help="Service is required")
service_package_parser.add_argument('package_name', type=str, required=True, help="Service Package is required")
service_package_parser.add_argument('cost', type=int, required = True, help="Cost is required")
service_package_parser.add_argument('description', type=str, required=False)

#Service Request Parser
service_request_parser = reqparse.RequestParser()
service_request_parser.add_argument('package_id', type=int, required=True, help="Service Package is required")
service_request_parser.add_argument('user_id', type=int, required=True, help="User is required")
service_request_parser.add_argument('professional_id', type=int, required=True, help="Service Professional is required")

service_request_edit_parser = reqparse.RequestParser()
service_request_edit_parser.add_argument('remarks', type=str, required=False)
service_request_edit_parser.add_argument('rating', type=int, required=False, help="Please give proper rating")
service_request_edit_parser.add_argument('service_status', type=str)

class UserResource(Resource):

    def post(self):
    # Parse input arguments
        args = user_parser.parse_args()
        username = args['username']
        password = args['password']
        role_name = args['role_name']

        # Check if the username or email already exists
        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400

        # Retrieve role by name
        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            return {"message": "Role not found"}, 404

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # Create new user
        new_user = User(
            username=username,
            password=hashed_password,
            role_id=role.role_id
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User created successfully", "user_id": new_user.user_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while creating the user", "error": str(e)}, 500
        
    @jwt_required()
    @role_required('admin', 'customer')
    def get(self):
        users = User.query.all()
        users_response = [user.to_dict(True) for user in users]
        return users_response, 200
        
# Login Resource
class LoginResource(Resource): 
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']

        # Fetch user by email
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid email or password"}, 401

        # Fetch user role
        role = Role.query.get(user.role_id)
        if not role:
            return {"message": "User role not found"}, 404
        
        if role.role_name == 'professional':
            professional = Service_Professional.query.filter_by(user_id=user.user_id).first()
            if professional.status != 'accepted':
                return {"message": "Professional is blocked or rejected"}, 403
            if not professional:
                return {"message": "Professional not found"}, 404
        elif role.role_name == 'customer':
            customer = Customer.query.filter_by(user_id=user.user_id).first()
            if customer.status != 'active':
                return {"message": "Customer is blocked"}, 403
            if not customer:
                return {"message": "Customer not found"}, 404


        # Create JWT token
        import json
        access_token = create_access_token(identity=json.dumps({"user_id": user.user_id, "role_name": role.role_name}))

        return {"access_token": access_token, "user_id": user.user_id, "role": role.role_name}, 200

#  -----------------See if the block is useful-----------------
# Role-Based Resource
class RoleBasedResource(Resource):
    method_decorators = [jwt_required()] 

    def get(self, role_name):
        # Get current user's role from JWT
        current_user = get_jwt_identity()
        user_role = current_user.get('role_name')

        # Authorization check
        if user_role != role_name:
            return {"message": "Access denied: Unauthorized role"}, 403

        return {"message": f"Welcome, {user_role} user!"}, 200
#  ----------------------------Till this-----------------------   

class CustomerResource(Resource): 

    @jwt_required()
    @role_required('admin', 'customer')
    def get(self):
        customers = Customer.query.all()
        customers_response = [customer.to_dict(True) for customer in customers]
        return customers_response, 200

    def post(self):
        args = customer_parser.parse_args()
        user_id = args['user_id']
        email = args['email']
        name = args['name']
        mobile_no = args['mobile_no']
        address = args['address']
        pincode = args['pincode']
        city_id = args['city_id']
        role_name = 'customer'
        status = 'active'

        # Check if the username or email already exists
        if Customer.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        # Retrieve role by name
        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            return {"message": "Role not found"}, 404

        # Create new user
        new_customer = Customer(
            user_id = user_id,
            email=email,
            name=name,
            mobile_no=mobile_no,
            address=address,
            pincode=pincode,
            city_id=city_id,
            status=status
        )

        try:
            db.session.add(new_customer)
            db.session.commit()
            return {"message": "Customer created successfully", "customer_id": new_customer.customer_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while creating the customer", "error": str(e)}, 500

    @jwt_required()
    @role_required('admin')
    def put(self, customer_id):
        args = user_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        name = args['name']
        mobile_no = args['mobile_no']
        address = args['address']
        pincode = args['pincode']
        role_name = 'customer'

        # Check if the username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {"message": "Username or email already exists"}, 400
        
        # Retrieve role by name
        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            return {"message": "Role not found"}, 404
        
        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # Create new user
        user = User.query.get(customer_id)
        user.username = username
        user.email = email
        user.password = hashed_password
        user.name = name
        user.mobile_no = mobile_no
        user.address = address
        user.pincode = pincode
        user.role_id = role.role_id

        try:
            db.session.commit()
            return {"message": "Customer updated successfully", "user_id": user.user_id}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while updating the customer", "error": str(e)}, 500
        
    @role_required('admin')
    @jwt_required
    def delete(self, customer_id):
        Customer.query.delete(customer_id)
        db.session.commit()
        return {"message": "Customer deleted successfully"}, 204
    
class ProfessionalResource(Resource):

    @jwt_required()
    @role_required('admin', 'professional')
    def get(self):
        professionals = Service_Professional.query.all()
        professionals_response = [professional.to_dict(True) for professional in professionals]
        return professionals_response, 200

    def post(self):
        args = professional_parser.parse_args()
        user_id = args['user_id']
        email = args['email']
        name = args['name']
        mobile_no = args['mobile_no']
        address = args['address']
        pincode = args['pincode']
        city_id = args['city_id']
        role_name = 'professional'
        experience = args['experience']
        service_id = args['service_id']
        #id_pdf = args['id_proof']
        status = 'requested'

        # Process file upload
        id_pdf_file = request.files.get('id_document')  # Get file from request
        id_pdf_data = id_pdf_file.read() if id_pdf_file else None  # Read file data

        # Check if the username or email already exists
        if Service_Professional.query.filter_by(email=email).first():
            return {"message": "Email already exists"}, 400

        # Retrieve role by name
        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            return {"message": "Role not found"}, 404

        # Create new user
        new_customer = Service_Professional(
            user_id = user_id,
            email=email,
            name=name,
            mobile_no=mobile_no,
            address=address,
            pincode=pincode,
            city_id=city_id,
            status=status,
            experience=experience,
            service_id=service_id,
            id_pdf=id_pdf_data
        )

        try:
            db.session.add(new_customer)
            db.session.commit()
            return {"message": "Service Professional created successfully", "professional_id": new_customer.professional_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while creating the service professional", "error": str(e)}, 500
        
class ServiceResource(Resource): 

    def get(self, service_id=None):
        if service_id is None:
            # Fetch all services
            services = Service.query.all()
            return [service.to_dict(False) for service in services], 200
        else:
            # Fetch a single service by ID
            service = Service.query.get(service_id)
            if not service:
                return {"message": "Service not found"}, 404
            return service.to_dict(False), 200
        
    @jwt_required()
    @role_required('admin')
    def post(self):
        args = service_parser.parse_args()
        service_name = args['service_name']
        time_required = args['time_required']
        description = ''
        if args['description']:
            description = args['description']

        services = Service.query.filter(Service.service_name == service_name)
        if services.count() == 0:
            db.session.add(Service(
                service_name=service_name, 
                time_required=time_required, 
                description=description))
            db.session.commit()
        else:
            return {"message": "Service already exists!!"}, 400
        
        return {"message": "Service created successfully!!"}, 201

    @jwt_required()
    @role_required('admin')
    def put(self, service_id):
        args = service_parser.parse_args()
        service_name = args['service_name']
        time_required = args['time_required']
        description = ''
        if args['description']:
            description = args['description']
        try:
            service = Service.query.get(service_id)
            
            service.service_name = service_name
            service.time_required = time_required
            service.description = description
            db.session.commit()
        
            return {"message": "Service updated successfully!!"}, 200
        except Exception as e:
            return {"message": "Service is not updated", "error": str(e)}, 500

    @jwt_required()
    @role_required('admin')
    def delete(self, service_id):
        try:
            service = Service.query.get(service_id)
            if not service:
                return {"message": "Service not found"}, 404
            
            db.session.delete(service)
            db.session.commit()
            return {"message": "Service deleted successfully"}, 204
        except Exception as e:
            db.session.rollback()  # Rollback in case of failure
            return {"message": "Service is not deleted", "error": str(e)}, 500
        
class ServicePackageResource(Resource):
    method_decorators = [jwt_required()] 

    @role_required('admin', 'customer')
    def get(self, package_id=None):
        if package_id is None:
            # Fetch all service packages
            service_packages = Service_Package.query.all()
            return [package.to_dict(False) for package in service_packages], 200
        else:
            # Fetch a single package by ID
            service_package = Service_Package.query.get(package_id)
            if not service_package:
                return {"message": "Service package not found"}, 404
            return service_package.to_dict(False), 200

    @role_required('admin')
    def post(self):
        args = service_package_parser.parse_args()
        service_id = args['service_id']
        package_name = args['package_name']
        cost = args['cost']
        description = ''
        if args['description']:
            description = args['description']

        packages = Service_Package.query.filter(Service_Package.package_name == package_name)
        if packages.count() == 0:
            db.session.add(Service_Package(
                service_id=service_id,
                package_name=package_name, 
                cost=cost, 
                description=description))
            db.session.commit()
        else:
            return {"message": "Service Package already exists!!"}, 400
        
        return {"message": "Service Package created successfully!!"}, 201

    @role_required('admin')
    def put(self, package_id):
        args = service_package_parser.parse_args()
        package_name = args['package_name']
        cost = args['cost']
        description = ''
        if args['description']:
            description = args['description']
        try:

            package = Service_Package.query.get(package_id)
        
            package.package_name = package_name
            package.cost = cost
            package.description = description
            db.session.commit()
        
            return {"message": "Service Package updated successfully!!"}, 200
        except Exception as e:
            return {"message": "Service Package is not updated", "error": str(e)}, 500

    @role_required('admin')
    def delete(self, package_id):
        try:
            package = Service_Package.query.get(package_id)
            if not package:
                return {"message": "Service Package not found"}, 404
            
            db.session.delete(package)
            db.session.commit()
            return {"message": "Service Package deleted successfully"}, 204
        except Exception as e:
            db.session.rollback()  # Rollback in case of failure
            return {"message": "Service Package is not deleted", "error": str(e)}, 500
    
class ServiceRequestResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin', 'customer', 'professional')
    def get(self):
        requests = Service_Request.query.all()
        requests_response = [request.to_dict(True) for request in requests]
        return requests_response, 200
    
    @role_required('customer')
    def post(self):
        args = service_request_parser.parse_args()
        package_id = args['package_id']
        user_id = args['user_id']
        professional_id = args['professional_id']
        request_date = date.today()
        service_status = 'requested'

        customer_id = Customer.query.filter_by(user_id = user_id).first().customer_id
        db.session.add(Service_Request(
            package_id=package_id,
            customer_id=customer_id,
            professional_id=professional_id,
            request_date=request_date,
            service_status=service_status))
        db.session.commit()
        
        return {"message": "Service Request created successfully!!"}, 201
    
    @role_required('customer')
    def put(self, request_id):
        args = service_request_edit_parser.parse_args()
        remarks = args['remarks']
        rating = args['rating']
        service_status = args['service_status']

        try:
            request = Service_Request.query.get(request_id)
            request.remarks = remarks
            request.service_rating = rating
            if service_status:
                request.service_status = service_status
            db.session.commit()

            return {"message": "Service Request updated successfully!!"}, 200
        except Exception as e:
            return {"message": "Service Request not updated!!"}, 400
    
class AcceptRequestResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('professional')
    def put(self, request_id):
        request = Service_Request.query.get(request_id)
        if request:
            request.service_status = 'in-progress'
            db.session.commit()
            return {"message": "Request accepted successfully"}, 200
        else:
            return {"message": "Request not found"}, 404
        
class RejectRequestResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('professional')
    def put(self, request_id):
        request = Service_Request.query.get(request_id)
        if request:
            request.service_status = 'rejected'
            db.session.commit()
            return {"message": "Request rejected successfully"}, 200
        else:
            return {"message": "Request not found"}, 404
        
class CloseRequestResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('professional', 'customer')
    def put(self, request_id):
        request = Service_Request.query.get(request_id)
        if request:
            request.service_status = 'closed'
            request.complete_date = date.today().strftime("%d-%m-%Y")
            db.session.commit()
            return {"message": "Request closed successfully"}, 200
        else:
            return {"message": "Request not found"}, 404
        
class AcceptProfessionalResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin')
    def put(self, professional_id):
        professional = Service_Professional.query.get(professional_id)
        if professional:
            professional.status = 'accepted'
            db.session.commit()
            return {"message": "Professional accepted successfully"}, 200
        else:
            return {"message": "Professional not found"}, 404
        
class RejectProfessionalResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin')
    def put(self, professional_id):
        professional = Service_Professional.query.get(professional_id)
        if professional:
            professional.status = 'rejected'
            db.session.commit()
            return {"message": "Professional rejected successfully"}, 200
        else:
            return {"message": "Professional not found"}, 404
        
class BlockProfessionalResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin')
    def put(self, professional_id):
        professional = Service_Professional.query.get(professional_id)
        if professional:
            professional.status = 'blocked'
            db.session.commit()
            return {"message": "Professional blocked successfully"}, 200
        else:
            return {"message": "Professional not found"}, 404
        
class UnblockProfessionalResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin')
    def put(self, professional_id):
        professional = Service_Professional.query.get(professional_id)
        if professional:
            professional.status = 'accepted'
            db.session.commit()
            return {"message": "Professional unblocked successfully"}, 200
        else:
            return {"message": "Professional not found"}, 404
        
class BlockCustomerResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin')
    def put(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            customer.status = 'blocked'
            db.session.commit()
            return {"message": "Customer blocked successfully"}, 200
        else:
            return {"message": "Customer not found"}, 404
        
class UnblockCustomerResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin')
    def put(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            customer.status = 'active'
            db.session.commit()
            return {"message": "Customer unblocked successfully"}, 200
        else:
            return {"message": "Customer not found"}, 404
        
class AcceptServiceRequestResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('professional')
    def put(self, request_id):
        request = Service_Request.query.get(request_id)
        if request:
            request.service_status = 'in-progress'
            db.session.commit()
            return {"message": "Service Request accepted successfully"}, 200
        else:
            return {"message": "Service Request not found"}, 404
        
class RejectServiceRequestResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('professional')
    def put(self, request_id):
        request = Service_Request.query.get(request_id)
        if request:
            request.service_status = 'rejected'
            db.session.commit()
            return {"message": "Service Request rejected successfully"}, 200
        else:
            return {"message": "Service Request not found"}, 404

class ServiceRequestByProfessionalResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('professional')
    def get(self, user_id):
        professional_id = Service_Professional.query.filter_by(user_id=user_id).first().professional_id
        requests = Service_Request.query.filter(Service_Request.professional_id == professional_id).all()
        requests_response = [request.to_dict(True) for request in requests]
        return requests_response, 200
    
class ServiceRequestByCustomerResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('customer')
    def get(self, user_id):
        customer_id = Customer.query.filter_by(user_id=user_id).first().customer_id
        requests = Service_Request.query.filter(Service_Request.customer_id == customer_id).all()
        requests_response = [request.to_dict(True) for request in requests]
        return requests_response, 200
    
class ServiceAvailableForCustomerResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('customer')
    def get(self, user_id):
        customer = Customer.query.filter_by(user_id=user_id).first()
        # Fetch services where service professionals are in the same city as the customer
        services = (
            db.session.query(Service)
            .join(Service_Professional, Service.service_id == Service_Professional.service_id)
            .filter(Service_Professional.city_id == customer.city_id)  # Match customer city
            .distinct()
            .all()
        )
        services_response = [service.to_dict(False) for service in services]
        return services_response, 200

class ServicePackagesByServiceResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin', 'customer')
    def get(self, service_id):
        packages = Service_Package.query.filter_by(service_id=service_id).all()
        packages_response = [package.to_dict(False) for package in packages]
        return packages_response, 200
    
class ServiceProfessionalsForCustomers(Resource):
    method_decorators = [jwt_required()]

    @role_required('customer')
    def get(self, customer_id, service_id):
        try:
            # Fetch customer details to get city_id
            customer = Customer.query.filter_by(customer_id=customer_id).first()

            if not customer:
                return jsonify({"error": "Customer not found"}), 404

            # Fetch professionals who provide the given service and are in the same city
            professionals = Service_Professional.query.filter(Service_Professional.service_id == service_id and Service_Professional.city_id == customer.city_id).all()
            

            return [professional.to_dict(True) for professional in professionals]
        except Exception as e:
            return {"message": "Professionals are not get", "error": str(e)}, 500
        
    
class CityResource(Resource):
    def get(self):
        cities = City.query.all()

        return [city.to_dict(False) for city in cities], 200
# class ExportReportResource(Resource):
#     method_decorators = [jwt_required()]
#     def post(self):
#         from tasks import export_closed_service_requests
#         admin = User.query.filter_by(role_id=1).first()
#         export_closed_service_requests.delay(admin.email)  # Runs in the background
#         return jsonify({"message": "CSV export job started. You'll receive an email once done."}), 200