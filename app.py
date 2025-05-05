import celery
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
from worker import celery_init_app
from celery import shared_task
from flask_mail import Message
from models import *
import csv
import requests
from datetime import datetime, timedelta


# Initialize Flask app and extensions
app = Flask(__name__)
CORS(app,
     origins=[
         "https://localhost:8080",
         "https://studious-tribble-wprp65v6749h9p54-8080.app.github.dev"
     ],
     supports_credentials=True)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///HousingServiceDB.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'ThisIsASecretKey' # Replace with a secure key
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

mail = Mail(app)
mail.init_app(app)
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def celery_job(sender,**kwargs):
    #sender.add_periodic_task(crontab(hour=12, minute=21, day_of_month=5), monthly_reminder.s())
    #sender.add_periodic_task(crontab(hour=12, minute=21), daily_remainder.s())

    #for testing
    sender.add_periodic_task(300,daily_reminder_job.s())
    sender.add_periodic_task(300,monthly_activity_report.s())

db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

# Add resources
api.add_resource(LoginResource, '/api/login')
api.add_resource(RoleBasedResource, '/api/role-based/<string:role_name>')
api.add_resource(UserResource, '/api/user')
api.add_resource(ProfessionalResource, '/api/professional')
api.add_resource(ServiceResource, "/api/service", "/api/service/<int:service_id>")
api.add_resource(ServicePackageResource, "/api/service-package", "/api/service-package/<int:package_id>")
api.add_resource(CustomerResource, '/api/customer')
api.add_resource(ServiceRequestResource, '/api/service-request', '/api/service-request/<int:request_id>')
api.add_resource(AcceptProfessionalResource, "/api/professional/<int:professional_id>/accept")
api.add_resource(RejectProfessionalResource, "/api/professional/<int:professional_id>/reject")
api.add_resource(BlockProfessionalResource, "/api/professional/<int:professional_id>/block")
api.add_resource(UnblockProfessionalResource, "/api/professional/<int:professional_id>/unblock")
api.add_resource(BlockCustomerResource, "/api/customer/<int:customer_id>/block")
api.add_resource(UnblockCustomerResource, "/api/customer/<int:customer_id>/unblock")
api.add_resource(AcceptServiceRequestResource, "/api/service-request/<int:request_id>/accept")
api.add_resource(RejectServiceRequestResource, "/api/service-request/<int:request_id>/reject")
api.add_resource(ServiceRequestByProfessionalResource, "/api/professional/<int:user_id>/service-request")
api.add_resource(ServiceRequestByCustomerResource, "/api/customer/<int:user_id>/service-request")
api.add_resource(ServiceAvailableForCustomerResource, "/api/customer/<int:user_id>/services")
api.add_resource(ServicePackagesByServiceResource, "/api/service/<int:service_id>/service-package")
api.add_resource(CityResource, "/api/cities")
api.add_resource(ServiceProfessionalsForCustomers, "/api/customer/<int:customer_id>/professionals/<int:service_id>")
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
        admin = User(role_id=admin_role.role_id, username='admin', password=generate_password_hash('adminPassword', method='pbkdf2:sha256', salt_length=16))
        
        # Insert Customer
        customers = [
            User(role_id=customer_role.role_id, username='john_doe', password=generate_password_hash('custPassword', method='pbkdf2:sha256', salt_length=16)),
            User(role_id=customer_role.role_id, username='robert_greens', password=generate_password_hash('custPassword', method='pbkdf2:sha256', salt_length=16))
        ]
        
        
        # Insert Service Professionals
        professionals = [
            User(role_id=professional_role.role_id, username='alice_smith', password=generate_password_hash('profPassword', method='pbkdf2:sha256', salt_length=16)),
            User(role_id=professional_role.role_id, username='bob_jones', password=generate_password_hash('profPassword', method='pbkdf2:sha256', salt_length=16))
        ]
        
        db.session.add_all([admin] + customers + professionals)
        db.session.commit()
        
        # Insert Services
        services = [Service(service_name='Plumbing', time_required=60, description='Plumbing services'),
                    Service(service_name='Electrical', time_required=90, description='Electrical repair')]
        db.session.add_all(services)
        db.session.commit()

        cities = [City(city_name='Mumbai'), 
                  City(city_name='Pune'),
                  City(city_name='Delhi'),
                  City(city_name='Banglore'),
                  City(city_name='Nagpur'),
                  City(city_name='Kolkata'),
                  City(city_name='Chennai'),
                  City(city_name='Hyderabad')]
        db.session.add_all(cities)
        db.session.commit()
        
        # Assign Service Professionals
        service_professionals = [
            Service_Professional(user_id=professionals[0].user_id, service_id=services[0].service_id, email='alice.smith@example.com',
                                 city_id = cities[0].city_id, name='Alice Smith', mobile_no=1112223333, experience=5, status='accepted'),
            Service_Professional(user_id=professionals[1].user_id, service_id=services[1].service_id, email='bob.jones@example.com', 
                                 city_id = cities[1].city_id, name='Bob Jones', mobile_no=4445556666, experience=7, status='accepted')
        ]
        db.session.add_all(service_professionals)
        db.session.commit()
        
        # Insert Customer Entry
        # Assign Service Professionals
        customer_data = [
            Customer(user_id=customers[0].user_id, email='aryachvn2002@gmail.com', city_id = cities[0].city_id, 
                     name='John Doe', mobile_no=9876543210, status='active'),
            Customer(user_id=customers[1].user_id, email='robert.greens@example.com', city_id = cities[1].city_id, 
                     name='Robert Greens', mobile_no=9876543210, status='blocked'),
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

# Google Chat Webhook URL
GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAQRoxTy4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=LVCxdmIOf_B6Qfw0VPzO8tWTOqWhnygK-pF50FTBScs"

@shared_task
def daily_reminder_job():
    """
    Sends reminders to service professionals who have pending service requests.
    """
    with app.app_context():
        pending_requests = (
            db.session.query(Service_Professional)
            .join(Service_Request, Service_Request.professional_id == Service_Professional.professional_id)
            .filter(Service_Request.service_status == 'requested')
            .all()
        )

        for professional in pending_requests:
            user = User.query.get(professional.user_id)
            if user:
                message = {
                    "text": f"Reminder: You have pending service requests. Please review and take action."
                }
                requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=message)
    return "Daily reminders sent."

@shared_task
def monthly_activity_report():
    """
    Generates and sends a monthly activity report to customers.
    """
    with app.app_context():
        customers = Customer.query.all()
        for customer in customers:
            service_requests = Service_Request.query.filter_by(customer_id=customer.customer_id).all()
            report_content = "<h1>Monthly Activity Report</h1><ul>"
            for req in service_requests:
                report_content += f"<li>Service ID: {req.request_id}, Status: {req.service_status}, Date: {req.request_date}</li>"
            report_content += "</ul>"
            msg = Message("Your Monthly Activity Report", recipients=[customer.email], html=report_content)
            mail.send(msg)
    return "Monthly reports sent."

@celery_app.task(name="export_closed_service_requests")
def export_closed_service_requests():
    """
    Exports closed service requests to a CSV file.
    """
    # ✅ Use WSL-compatible path
    export_folder = os.path.join(app.root_path, "exports")
    print(export_folder, flush=True)

    # ✅ Create the folder if it doesn't exist
    try:
        if not os.path.exists(export_folder):
            os.makedirs(export_folder, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory: {e}")  # Debugging output

    filename = f"closed_requests_{datetime.now().strftime('%Y%m%d')}.csv"
    filepath = os.path.join(export_folder, filename)

    with app.app_context():
        closed_requests = Service_Request.query.filter_by(service_status='closed').all()
        print(closed_requests)
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Request ID", "Customer ID", "Professional ID", "Request Date", "Complete Date", "Remarks"])
            for req in closed_requests:
                writer.writerow([req.request_id, req.customer_id, req.professional_id, req.request_date, req.complete_date, req.remarks])

    print(f"CSV file created at: {filepath}")  # Debugging output
    return filepath  # Return the file path for later retrieval

@app.route('/api/export-csv', methods=['POST'])
def start_export():
    task = export_closed_service_requests.delay()   # Run task asynchronously
    return jsonify({"message": "Export started. Please download later.", "task_id": task.id})

@app.route('/api/download-csv', methods=['GET'])
def download_csv():
    # Get the latest CSV file
    export_dir = os.path.join(app.root_path, "exports")
    files = sorted(
        [f for f in os.listdir(export_dir) if f.endswith('.csv')],
        key=lambda x: os.path.getmtime(os.path.join(export_dir, x)),
        reverse=True
    )

    if not files:
        return jsonify({"error": "No exported file found. Please try again later."}), 404

    latest_file = os.path.join(export_dir, files[0])
    return send_file(latest_file, as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert_dummy_data()
    print("App running")
    app.run(host="0.0.0.0", port=5000, debug=True)
