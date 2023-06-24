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

        self.created_at = datetime.now() # audit