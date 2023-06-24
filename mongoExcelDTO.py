from datetime import datetime

class PersonDTO:
    def __init__(self):
        self.linkedin_url = ""
        self.email = ""
        self.connection_start_time = ""
        self.website_url = ""
        self.phone = ""
        self.address = ""
        self.birthday = ""
        self.company_name = ""
        self.job_title = ""
        self.fullname = ""
        self.user_role_description = ""

        self.created_at = datetime.now() # audit
    
    def to_dict(self):
        return self.__dict__