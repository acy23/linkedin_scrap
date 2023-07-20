from datetime import datetime

class PersonLinkedinUrlDTO:
    def __init__(self):
        self._id = ""
        self.linkedin_url = ""
        self.firstname = ""
        self.lastname = ""

        self.created_at = datetime.now() # audit
        self.created_by = ""    
    def to_dict(self):
        return self.__dict__