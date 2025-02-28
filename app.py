from flask import Flask, render_template, redirect, request, url_for, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, func, or_
from datetime import date
from random import randint, choice
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from resources import *
from models import *
import os

# Initialize Flask app and extensions
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080", "supports_credentials": True}})
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///HousingServiceDB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback_secret') # Replace with a secure key
app.config['debug'] = True

db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

# Add resources
api.add_resource(LoginResource, '/login')
api.add_resource(RoleBasedResource, '/role-based/<string:role_name>')
api.add_resource(UserResource, '/user')
api.add_resource(ProfessionalResource, '/professional')
api.add_resource(ServiceResource, '/service')
api.add_resource(ServicePackageResource, '/service-package')
api.add_resource(CustomerResource, '/customer')

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
                     email='admin@example.com', name='Admin User', mobile_no=1234567890)
        
        # Insert Customer
        customer = User(role_id=customer_role.role_id, username='john_doe', password=generate_password_hash('custPassword', method='pbkdf2:sha256', salt_length=16),
                        email='john.doe@example.com', name='John Doe', mobile_no=9876543210)
        
        # Insert Service Professionals
        professionals = [
            User(role_id=professional_role.role_id, username='alice_smith', password=generate_password_hash('profPassword', method='pbkdf2:sha256', salt_length=16), 
                 email='alice.smith@example.com', name='Alice Smith', mobile_no=1112223333),
            User(role_id=professional_role.role_id, username='bob_jones', password=generate_password_hash('profPassword', method='pbkdf2:sha256', salt_length=16), 
                 email='bob.jones@example.com', name='Bob Jones', mobile_no=4445556666)
        ]
        
        db.session.add_all([admin, customer] + professionals)
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
        customer_entry = Customer(user_id=customer.user_id, status='unblocked')
        db.session.add(customer_entry)
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
                                  customer_id=customer_entry.customer_id, 
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