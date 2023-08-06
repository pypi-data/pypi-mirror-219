import re
import uuid

"""This is a singleton class that contains all the common variables and functions used in the project"""

# Codes for the different types of objects in the database
yd_uid_code = "YDUID"
yd_order_code = "YDORDER"
yd_request_code = "YDREQUEST"
yd_job_code = "YDJOB"
yd_offer_code = "YDOFFER"
yd_complaint_code = "YDCOMPLAINT"
yd_company_code = "YDCOMPANY"


class YDCommon(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(YDCommon, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if not YDCommon._instance:
            YDCommon._instance = YDCommon()
        return YDCommon._instance

    # Generates a random uid for the user
    @staticmethod
    def generate_uid():
        return uuid.uuid4().hex[:30]

    # Body handler for the request
    @staticmethod
    def get_body(request):
        return request.body.decode('utf-8')

    # Checks if the given string is a valid email
    @staticmethod
    def is_valid_email(email):
        # Check if the email matches email address format
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    # Checks if the given string is a valid phone number
    @staticmethod
    def is_valid_phone(phone):
        # Check if the phone matches phone number format
        if re.match(r"^\d{10}$", phone):
            return True
        return False

    # Check if request body is greater than 5MB
    @staticmethod
    def is_body_too_large(request):
        if len(request.body) > 5242880:
            return True
        return False

    # Check if the given string is a valid password
    @staticmethod
    def is_valid_password(password):
        # Check if the password matches password format
        if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
            return True
        return False

