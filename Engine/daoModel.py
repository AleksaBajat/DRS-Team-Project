from sqlalchemy import Column, Identity, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

class Register(Base):
    
    __tablename__ = "registrations"

    id = Column("id", Integer, Identity(start=1, cycle=True), primary_key=True)
    first_name = Column("firstName", String, nullable=True)
    last_name = Column("lastName", String, nullable=True)
    email = Column("email", String, nullable=True)
    address = Column("address", String, nullable=True)
    city = Column("city", String, nullable=True)
    country = Column("country", String, nullable=True)
    phone = Column("phone", String, nullable=True)
    password = Column("password", String, nullable=True)

    def __init__(self, first_name, last_name, email, address, city, country, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.password = password

class TransportType(Enum):
    REGISTER = 1
    LOGIN = 2

class StatusCode(Enum):
    SUCCESS = "SUCCESS"
    INTERNAL_SERVER_ERROR = "INTERNAL SERVER ERROR"
    NOT_FOUND = "NOT FOUND"
    ERROR = "ERROR"

class TransportData:
    def __init__(self, type, data):
        self.type = type
        self.data = data