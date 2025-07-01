from celery import shared_task
from flask_mail import Message
from models import *
from extensions import mail
import csv
import os
import requests
from datetime import datetime, timedelta

# Google Chat Webhook URL
GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/"  #Paste the gspace webhook link here

# @celery.task
# def daily_reminder_job():
#     """
#     Sends reminders to service professionals who have pending service requests.
#     """
#     with app.app_context():
#         pending_requests = (
#             db.session.query(Service_Professional)
#             .join(Service_Request, Service_Request.professional_id == Service_Professional.professional_id)
#             .filter(Service_Request.service_status == 'requested')
#             .all()
#         )

#         for professional in pending_requests:
#             user = User.query.get(professional.user_id)
#             if user:
#                 message = {
#                     "text": f"Reminder: You have pending service requests. Please review and take action."
#                 }
#                 requests.post(GOOGLE_CHAT_WEBHOOK_URL, json=message)
#     return "Daily reminders sent."

# @celery.task
# def monthly_activity_report():
#     """
#     Generates and sends a monthly activity report to customers.
#     """
#     with app.app_context():
#         customers = Customer.query.all()
#         for customer in customers:
#             user = User.query.get(customer.user_id)
#             if user:
#                 service_requests = Service_Request.query.filter_by(customer_id=customer.customer_id).all()
#                 report_content = "<h1>Monthly Activity Report</h1><ul>"
#                 for req in service_requests:
#                     report_content += f"<li>Service ID: {req.request_id}, Status: {req.service_status}, Date: {req.request_date}</li>"
#                 report_content += "</ul>"
#                 msg = Message("Your Monthly Activity Report", recipients=[user.email], html=report_content)
#                 mail.send(msg)
#     return "Monthly reports sent."

# @shared_task
# def export_closed_service_requests():
#     """
#     Exports closed service requests to a CSV file.
#     """
#     filename = f"closed_requests_{datetime.now().strftime('%Y%m%d')}.csv"
#     filepath = os.path.join("C:\\Users\\Arya Chavan", "exports", filename)
#     os.makedirs(os.path.dirname(filepath), exist_ok=True)

#     with app.app_context():
#         # Fetch closed service requests
#         closed_requests = Service_Request.query.filter_by(service_status='closed').all()
#         with open(filepath, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["Request ID", "Customer ID", "Professional ID", "Request Date", "Complete Date", "Remarks"])
#             for req in closed_requests:
#                 writer.writerow([req.request_id, req.customer_id, req.professional_id, req.request_date, req.complete_date, req.remarks])
#     return f"CSV export completed: {filename}"
