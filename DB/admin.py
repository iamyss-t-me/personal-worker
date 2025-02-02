from pymongo import MongoClient
from config import Config


class Admin:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client["project1"]
        self.collection = self.db["admin"]
    def update_worker(self, worker: bool):
        self.collection.update_one({"_id": "admin"}, {"$set": {"worker": worker}})
    
    def get_worker(self):
        return self.collection.find_one({"_id": "admin"}).get("worker")