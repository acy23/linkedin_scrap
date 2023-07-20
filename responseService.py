import json
from linkedinUrlsDTO import PersonLinkedinUrlDTO
from bson import ObjectId

from mongoService import MongoDBConnection

def remove_duplicates_by_linkedin_url(person_list):
    seen_linkedin_urls = set()
    unique_objects = []

    for person in person_list:
        if person.linkedin_url not in seen_linkedin_urls:
            seen_linkedin_urls.add(person.linkedin_url)
            unique_objects.append(person)
    return unique_objects

if(__name__ == '__main__'):

    # Specify the path to the downloaded file
    file_paths = ['esram77_0-1999.json',
                'esram77_2000-3358.json'
                ]

    encodings = ['utf-8', 'latin-1', 'cp1252']

    public_identifiers = []
    dataList = []

    for file_path in file_paths:

        # Read the file with different encodings until successful decoding
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    response = file.read()
                break  # Exit the loop if decoding is successful
            except UnicodeDecodeError:
                continue  # Try the next encoding

        # Parse the JSON response
        data = json.loads(response)

        for item in data.get('included', []):
            public_identifier = item.get('publicIdentifier')
            firstname = item.get('firstName')
            lastname = item.get('lastName')

            if(public_identifier and firstname and lastname):
                public_identifiers.append(public_identifier)

                linkedinUrlModel = PersonLinkedinUrlDTO()
                linkedinUrlModel._id = ObjectId() 
                linkedinUrlModel.linkedin_url = 'https://www.linkedin.com/in/' + public_identifier + '/'
                linkedinUrlModel.firstname = firstname
                linkedinUrlModel.lastname = lastname
                linkedinUrlModel.created_by = "esram77"

                dataList.append(linkedinUrlModel)

    distinct_objects = remove_duplicates_by_linkedin_url(dataList)

    connection = MongoDBConnection()
    connection.insert_many_documents("datacollection", distinct_objects)
