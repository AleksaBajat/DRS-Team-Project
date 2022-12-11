from enum import Enum

class TransportData:
    def __init__(self, type, data):
        self.type = type
        self.data = data


class TransportType(Enum):
    REGISTER = 1
    LOGIN = 2

class StatusCode(Enum):
    SUCCESS = "SUCCESS"
    INTERNAL_SERVER_ERROR = "INTERNAL SERVER ERROR"
    NOT_FOUND = "NOT FOUND"
    ERROR = "ERROR"

class RegisterDto():
    def __init__(self, first_name, last_name, email, address, city, country, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.password = password
