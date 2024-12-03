import os
from bson import ObjectId
from pymongo import MongoClient


class MongoAdapter:

    client = None

    def __init__(self):
        host = os.getenv("MONGO_HOST")
        port = os.getenv("MONGO_PORT")
        user = os.getenv("MONGO_USER")
        password = os.getenv("MONGO_PASSWORD")

        self.client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")

    def _database_connection(self, database_name="funexpression"):
        return self.client[database_name]

    def _get_collection(self, collection_name):
        db_conn = self._database_connection()

        return db_conn.get_collection(collection_name)

    def get_all(self, collection_name):
        collection = self._get_collection(collection_name)

        return collection.find()

    def get_by_id(self, collection_name, id):
        collection = self._get_collection(collection_name)

        return collection.find_one({"_id": ObjectId(id)})

    def create(self, collection_name, data):
        collection = self._get_collection(collection_name)
        result = collection.insert_one(data)

        return result.inserted_id

    def find(self, collection_name, query):
        collection = self._get_collection(collection_name)

        return collection.find(query).to_list()

    def update(self, collection_name, id, data):
        collection = self._get_collection(collection_name)
        return collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    def delete(self, collection_name, id):
        collection = self._get_collection(collection_name)
        return collection.delete_one({"_id": ObjectId(id)})

    def updateById(self, pipeline_id, object):
        collection = self._get_collection("pipelines")

        updated_collection = collection.update_one(
            {"_id": ObjectId(pipeline_id)}, {"$set": object}
        )

        return updated_collection.upserted_id
