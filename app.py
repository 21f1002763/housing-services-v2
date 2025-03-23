from flask import Flask, render_template, redirect, request, url_for, Response, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, func, or_
from datetime import date
from random import randint, choice
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from resources import *
from models import *
import os
from celery_worker import celery
from tasks import export_closed_service_requests
from extensions import mail


# Initialize Flask app and extensions
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///HousingServiceDB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback_secret') # Replace with a secure key
app.config['debug'] = True

# Celery Configuration
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

# Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Use your email provider
app.config["MAIL_PORT"] = 587  # Usually 587 for TLS, 465 for SSL
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "ayra.dummy@gmail.com"  # Replace with your email
app.config["MAIL_PASSWORD"] = "uope jwdz vbiq lrzg"  # Use App Password for Gmail
app.config["MAIL_DEFAULT_SENDER"] = "ayra.dummy@gmail.com"

mail.init_app(app)

db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

# Import Celery after app creation
celery.conf.update(app.config)

# Add resources
api.add_resource(LoginResource, '/api/login')
api.add_resource(RoleBasedResource, '/api/role-based/<string:role_name>')
api.add_resource(UserResource, '/api/user')
api.add_resource(ProfessionalResource, '/api/professional')
api.add_resource(ServiceResource, "/api/service", "/api/service/<int:service_id>")
api.add_resource(ServicePackageResource, '/api/service-package')
api.add_resource(CustomerResource, '/api/customer')
api.add_resource(ServiceRequestResource, '/api/service-request')
api.add_resource(AcceptProfessionalResource, "/api/professional/<int:professional_id>/accept")
api.add_resource(RejectProfessionalResource, "/api/professional/<int:professional_id>/reject")
api.add_resource(BlockProfessionalResource, "/api/professional/<int:professional_id>/block")
api.add_resource(UnblockProfessionalResource, "/api/professional/<int:professional_id>/unblock")
api.add_resource(BlockCustomerResource, "/api/customer/<int:customer_id>/block")
api.add_resource(UnblockCustomerResource, "/api/customer/<int:customer_id>/unblock")
# api.add_resource(ExportReportResource, "/api/admin/export_report")

# Handle expired tokens
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired", "status": 401}), 401

#add dummy data
def insert_dummy_data():
    with app.app_context():
        # Insert Roles
        admin_role = Role(role_name='admin', description='Administrator role')
        customer_role = Role(role_name='customer', description='Customer role')
        professional_role = Role(role_name='professional', description='Service provider role')
        db.session.add_all([admin_role, customer_role, professional_role])
        db.session.commit()
        
        # Insert Admin
        admin = User(role_id=admin_role.role_id, username='admin', password=generate_password_hash('adminPassword', method='pbkdf2:sha256', salt_length=16), 
                     email='aryachvn2002@gmail.com', name='Admin User', mobile_no=1234567890)
        
        # Insert Customer
        customers = [
            User(role_id=customer_role.role_id, username='john_doe', password=generate_password_hash('custPassword', method='pbkdf2:sha256', salt_length=16),
                        email='john.doe@example.com', name='John Doe', mobile_no=9876543210),
            User(role_id=customer_role.role_id, username='robert_greens', password=generate_password_hash('custPassword', method='pbkdf2:sha256', salt_length=16),
                        email='robert.greens@example.com', name='Robert Greens', mobile_no=9876543210)
        ]
        
        
        # Insert Service Professionals
        professionals = [
            User(role_id=professional_role.role_id, username='alice_smith', password=generate_password_hash('profPassword', method='pbkdf2:sha256', salt_length=16), 
                 email='alice.smith@example.com', name='Alice Smith', mobile_no=1112223333),
            User(role_id=professional_role.role_id, username='bob_jones', password=generate_password_hash('profPassword', method='pbkdf2:sha256', salt_length=16), 
                 email='bob.jones@example.com', name='Bob Jones', mobile_no=4445556666)
        ]
        
        db.session.add_all([admin] + customers + professionals)
        db.session.commit()
        
        # Insert Services
        services = [Service(service_name='Plumbing', time_required=60, description='Plumbing services'),
                    Service(service_name='Electrical', time_required=90, description='Electrical repair')]
        db.session.add_all(services)
        db.session.commit()
        
        # Assign Service Professionals
        service_professionals = [
            Service_Professional(user_id=professionals[0].user_id, service_id=services[0].service_id, 
                                 experience=5, status='accepted'),
            Service_Professional(user_id=professionals[1].user_id, service_id=services[1].service_id, 
                                 experience=7, status='accepted')
        ]
        db.session.add_all(service_professionals)
        db.session.commit()
        
        # Insert Customer Entry
        # Assign Service Professionals
        customer_data = [
            Customer(user_id=customers[0].user_id, status='active'),
            Customer(user_id=customers[1].user_id, status='blocked'),
        ]
        db.session.add_all(customer_data)
        db.session.commit()
        
        # Insert Service Packages
        packages = [
            Service_Package(service_id=services[0].service_id, package_name='Basic Plumbing',
                            cost=100, description='Basic plumbing services'),
            Service_Package(service_id=services[1].service_id, package_name='Standard Electrical',
                            cost=200, description='Standard electrical repair')
        ]
        db.session.add_all(packages)
        db.session.commit()
        
        # Insert Service Requests
        request = Service_Request(package_id=packages[0].package_id, 
                                  customer_id=customer_data[0].customer_id, 
                                  professional_id=service_professionals[0].professional_id,
                                  request_date=date.today(), 
                                  service_status='requested')
        db.session.add(request)
        db.session.commit()
        
        print("Dummy data inserted successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_dummy_data()
    print("App running")
    app.run(debug=True)