from flask import Flask, render_template, redirect, request, url_for, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, func, or_
from datetime import date
from random import randint, choice

db = SQLAlchemy()

from datetime import date, datetime

class BaseModel(db.Model):
    __abstract__ = True  # Prevents table creation for this class

    def to_dict(self, include_relationships=False):
        """Convert model instance to dictionary, handling date serialization."""
        result = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            # Convert `date` and `datetime` objects to string
            if isinstance(value, (date, datetime)):
                result[column.name] = value.isoformat()  # Converts to "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS"
            else:
                result[column.name] = value

        if include_relationships:
            for relationship in self.__mapper__.relationships:
                related_obj = getattr(self, relationship.key)
                if related_obj is None:
                    result[relationship.key] = None
                elif isinstance(related_obj, list):
                    result[relationship.key] = [obj.to_dict() for obj in related_obj]
                else:
                    result[relationship.key] = related_obj.to_dict()

        return result


class Role(BaseModel):
    __tablename__ = 'role'  
    role_id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    role_name = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.String, nullable = True)

class User(BaseModel):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    name = db.Column(db.String, nullable = False)
    mobile_no = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String , nullable = True)
    pincode = db.Column(db.Integer, nullable = True)
    user_roles = db.relationship("Role", backref = "user")

class Service_Professional(BaseModel):
    __tablename__ = 'service_professional'
    professional_id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'))
    experience = db.Column(db.Integer, nullable = False)
    id_pdf = db.Column(db.LargeBinary, nullable=True)
    status = db.Column(Enum('accepted', 'rejected', 'requested', 'blocked',  name='professional_status_enum'), nullable=False, default='requested')
    service = db.relationship("Service", backref = "service_professional")
    user = db.relationship("User", backref="service_professional")
    service = db.relationship("Service", backref="service_professionals")

class Customer(BaseModel):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    status = db.Column(Enum('blocked', 'unblocked',  name='customer_status_enum'), nullable=False, default='requested')
    user = db.relationship("User", backref = "customer")

class Service(BaseModel):
    __tablename__ = 'service'
    service_id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    service_name = db.Column(db.String, nullable = False, unique = True)
    time_required = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable = True)

class Service_Package(BaseModel):
    __tablename__ = 'service_package'
    package_id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.service_id'))
    package_name = db.Column(db.String, nullable = False, unique = True)
    cost = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable = True)
    package_services = db.relationship("Service", backref = "service_package")

class Service_Request(BaseModel):
    __tablename__ = 'service_reqeust'
    request_id = db.Column(db.Integer, primary_key = True, autoincrement = True, nullable = False)
    package_id = db.Column(db.Integer, db.ForeignKey('service_package.package_id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.professional_id'))
    request_date = db.Column(db.Date, nullable = False)
    complete_date = db.Column(db.Date, nullable = True)
    service_status = db.Column(Enum('in-progress', 'rejected', 'requested', 'closed',  name='service_status_enum'), nullable=False, default='requested')
    service_rating = db.Column(db.Integer, nullable = True)
    remarks = db.Column(db.String, nullable = True, default = 0)
    packages = db.relationship("Service_Package", backref="service_reqeust")
    customers = db.relationship("Customer", backref="service_reqeust")
    professionals = db.relationship("Service_Professional", backref="service_reqeust")