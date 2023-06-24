from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, connection_uri = "mongodb+srv://acy:linkedinscrap2023@linkedinscrap.07crxyr.mongodb.net"):
        self.client = MongoClient(connection_uri)
        self.db = self.client["linkedinscrap"]

    def insert_document(self, collection_name, data):
        collection = self.db[collection_name]
        collection.insert_one(data)

    def insert_many_documents(self, collection_name, data_list):
        collection = self.db[collection_name]
        documents = [data.to_dict() for data in data_list]
        collection.insert_many(documents)

"""
if __name__ == '__main__':
    connection = MongoDBConnection()
    my_object = MyClassModel('value1', 'value2')

    connection.insert_document('your_collection_name', my_object.to_dict())
"""