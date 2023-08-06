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
