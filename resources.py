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
user_parser.add_argument('username', type=str, required=True, help="Username is required")
user_parser.add_argument('email', type=str, required=True, help="Email is required")
user_parser.add_argument('password', type=str, required=True, help="Password is required")
user_parser.add_argument('name', type=str, required=True, help="Name is required")
user_parser.add_argument('mobile_no', type=int, required=True, help="Mobile number is required")
user_parser.add_argument('address', type=str, required=False)
user_parser.add_argument('pincode', type=int, required=False)
user_parser.add_argument('role_name', type=str, required=True, help="Role name is required")

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
service_request_parser.add_argument('customer_id', type=int, required=True, help="Customer is required")
service_request_parser.add_argument('professional_id', type=int, required=True, help="Service Professional is required")
service_request_parser.add_argument('request_date', type=date, required=True, help="Request Date is required")
service_request_parser.add_argument('service_status', type=str, required=True, help="Status is required")

class UserResource(Resource):
    method_decorators = [jwt_required()] 

    def post(self):
    # Parse input arguments
        args = user_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        name = args['name']
        mobile_no = args['mobile_no']
        address = args['address']
        pincode = args['pincode']
        role_name = args['role_name']

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
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            name=name,
            mobile_no=mobile_no,
            address=address,
            pincode=pincode,
            role_id=role.role_id
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User created successfully", "user_id": new_user.user_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while creating the user", "error": str(e)}, 500
        
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

        # Create JWT token
        import json
        access_token = create_access_token(identity=json.dumps({"user_id": user.user_id, "role_name": role.role_name}))

        return {"access_token": access_token, "role": role.role_name}, 200

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
    method_decorators = [jwt_required()] 

    @role_required('admin', 'customer')
    def get(self):
        customers = Customer.query.all()
        customers_response = jsonify([customer.to_dict() for customer in customers])
        return customers_response, 200

    @role_required('admin')
    def post(self):
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
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            name=name,
            mobile_no=mobile_no,
            address=address,
            pincode=pincode,
            role_id=role.role_id
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            db.session.add(Customer(user_id=new_user.user_id))
            db.session.commit()
            return {"message": "Customer created successfully", "user_id": new_user.user_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while creating the customer", "error": str(e)}, 500

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
    def delete(self, customer_id):
        Customer.query.delete(customer_id)
        db.session.commit()
        return {"message": "Customer deleted successfully"}, 204
    
class ProfessionalResource(Resource):
    method_decorators = [jwt_required()] 

    @role_required('admin', 'professional')
    def get(self):
        professionals = Service_Professional.query.all()
        professionals_response = [professional.to_dict(True) for professional in professionals]
        return professionals_response, 200

    @role_required('admin')
    def post(self):
        args = user_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        name = args['name']
        mobile_no = args['mobile_no']
        address = args['address']
        pincode = args['pincode']
        role_name = 'professional'

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
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            name=name,
            mobile_no=mobile_no,
            address=address,
            pincode=pincode,
            role_id=role.role_id
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            db.session.add(Service_Professional(user_id=new_user.user_id))
            db.session.commit()
            return {"message": "Professional created successfully", "user_id": new_user.user_id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while creating the professional", "error": str(e)}, 500

    @role_required('admin')
    def put(self, professional_id):
        args = user_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']
        name = args['name']
        mobile_no = args['mobile_no']
        address = args['address']
        pincode = args['pincode']
        role_name = 'professional'

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
        user = User.query.get(professional_id)
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
            return {"message": "Professional updated successfully", "user_id": user.user_id}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while updating the professional", "error": str(e)}, 500

class ServiceResource(Resource):
    method_decorators = [jwt_required()] 

    @role_required('admin', 'customer')
    def get(self):
        services = Service.query.all()
        services_response = jsonify([service.to_dict() for service in services])
        return services_response, 200

    @role_required('admin')
    def post(self):
        args = service_parser.parse_args()
        service_name = args['service_name']
        time_required = args['time_required']
        description = ''
        if args['description']:
            description = args['description']

        services = Service.query.filter(Service.service_name == service_name)
        if not services:
            db.session.add(Service(
                service_name=service_name, 
                time_required=time_required, 
                description=description))
            db.session.commit()
        else:
            return {"message": "Service already exists!!"}, 400
        
        return {"message": "Service created successfully!!"}, 201

    @role_required('admin')
    def put(self, service_id):
        args = service_parser.parse_args()
        service_name = args['service_name']
        time_required = args['time_required']
        description = ''
        if args['description']:
            description = args['description']

        service = Service.query.get(service_id)
        existing_service = Service.query.filter(Service.service_name == service_name and Service.service_id != service_id)
        if not existing_service:
            service.service_name = service_name
            service.time_required = time_required
            service.description = description
            db.session.commit()
        else:
            return {"message": "Service name already exists!!"}, 400
        
        return {"message": "Service updated successfully!!"}, 200

    @role_required('admin')
    def delete(self, service_id):
        Service.query.delete(service_id)
        db.session.commit()
        return {"message": "Service deleted successfully"}, 204

class ServicePackageResource(Resource):
    method_decorators = [jwt_required()] 

    @role_required('admin', 'customer')
    def get(self):
        packages = Service_Package.query.all()
        packages_response = jsonify([package.to_dict() for package in packages])
        return packages_response, 200

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
        if not packages:
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

        package = Service_Package.query.get(package_id)
        existing_pacakge = Service_Package.query.filter(
            Service_Package.package_name_name == package_name and Service_Package.package_id != package_id)
        if not existing_pacakge:
            package.package_name = package_name
            package.cost = cost
            package.description = description
            db.session.commit()
        else:
            return {"message": "Service Package name already exists!!"}, 400
        
        return {"message": "Service Package updated successfully!!"}, 200

    @role_required('admin')
    def delete(self, package_id):
        Service_Package.query.delete(package_id)
        db.session.commit()
        return {"message": "Service Package deleted successfully"}, 204
    
class ServiceRequestResource(Resource):
    method_decorators = [jwt_required()]

    @role_required('admin', 'customer', 'professional')
    def get(self):
        requests = Service_Request.query.all()
        requests_response = jsonify([request.to_dict() for request in requests])
        return requests_response, 200
    
    @role_required('customer')
    def post(self):
        args = service_request_parser.parse_args()
        package_id = args['package_id']
        customer_id = args['customer_id']
        professional_id = args['professional_id']
        request_date = date.today().strftime("%d-%m-%Y")
        service_status = 'requested'

        requests = Service_Request.query.filter(
            Service_Request.package_id == package_id and 
            Service_Request.customer_id == customer_id and
            Service_Request.service_status != 'closed')
        if not requests:
            db.session.add(Service_Request(
                package_id=package_id,
                customer_id=customer_id,
                professional_id=professional_id,
                request_date=request_date,
                service_status=service_status))
            db.session.commit()
        else:
            return {"message": "Service Request already exists!!"}, 400
        
        return {"message": "Service Request created successfully!!"}, 201
    
    @role_required('customer')
    def put(self, request_id):
        args = service_request_parser.parse_args()
        package_id = args['package_id']
        customer_id = args['customer_id']
        professional_id = args['professional_id']

        request = Service_Request.query.get(request_id)
        existing_request = Service_Request.query.filter(
            Service_Request.package_id == package_id and 
            Service_Request.customer_id == customer_id and 
            Service_Request.professional_id == professional_id and 
            Service_Request.request_id != request_id)
        if not existing_request:
            request.package_id = package_id
            request.customer_id = customer_id
            request.professional_id = professional_id
            db.session.commit()
        else:
            return {"message": "Service Request already exists!!"}, 400
        
        return {"message": "Service Request updated successfully!!"}, 200
    
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

    @role_required('professional')
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
            customer.status = 'unblocked'
            db.session.commit()
            return {"message": "Customer unblocked successfully"}, 200
        else:
            return {"message": "Customer not found"}, 404