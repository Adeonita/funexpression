class MongoAdapter:

    def __init__(self, mongo_client):
        self.client = mongo_client

    def get_collection(self, collection_name):
        return self.client[collection_name]

    def get_all(self, collection_name):
        collection = self.get_collection(collection_name)
        return collection.find()

    def get_by_id(self, collection_name, id):
        collection = self.get_collection(collection_name)
        return collection.find_one({"_id": ObjectId(id)})

    def insert(self, collection_name, data):
        collection = self.get_collection(collection_name)
        return collection.insert_one(data)

    def update(self, collection_name, id, data):
        collection = self.get_collection(collection_name)
        return collection.update_one({"_id": ObjectId(id)}, {"$set": data})

    def delete(self, collection_name, id):
        collection = self.get_collection(collection_name)
        return collection.delete_one({"_id": ObjectId(id)})
