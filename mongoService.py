from pymongo import MongoClient
from bson import ObjectId

class MongoDBConnection:
    def __init__(self, connection_uri = "mongodb+srv://acy:linkedinscrap2023@linkedinscrap.07crxyr.mongodb.net"):
        self.client = MongoClient(connection_uri)
        self.db = self.client["linkedinscrap"]

    def insert_document(self, collection_name, data):
        collection = self.db[collection_name]
        collection.insert_one(data)

    def insert_many_documents(self, collection_name, data_list):
        collection = self.db[collection_name]
        documents = [data.to_dict() for data in data_list if data is not None]
        collection.insert_many(documents)
        
    def get_all_documents(self, collection_name):
        collection = self.db[collection_name]
        documents = list(collection.find())
        return documents
    
    def get_documents_by_creator(self, collection_name, creator):
        collection = self.db[collection_name]
        query = {"created_by": creator}
        documents = list(collection.find(query))
        return documents