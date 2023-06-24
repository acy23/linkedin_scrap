from datetime import datetime

class PersonDTO:
    def __init__(self, linkedin_url, email, connection_start_time, website_url, phone, address, birthday):
        self.linkedin_url = linkedin_url
        self.email = email
        self.connection_start_time = connection_start_time
        self.website_url = website_url
        self.phone = phone
        self.address = address
        self.birthday = birthday

        self.created_at = datetime.now() # audit