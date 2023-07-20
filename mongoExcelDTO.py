from datetime import datetime

class PersonDTO:
    def __init__(self):
        self.linkedin_url = ""
        self.email = ""
        self.website_url = ""
        self.phone = ""
        self.address = ""
        self.day = ""
        self.month = ""
        #self.company_name = ""
        #self.last_experince_info = ""
        self.firstname = ""
        self.lastname = ""
        self.headline = ""
        self.profile_picture_url = ""

        self.created_at = datetime.now() # audit
        self.created_by = ""    
    def to_dict(self):
        return self.__dict__