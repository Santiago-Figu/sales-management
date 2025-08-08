from pymongo import MongoClient
from app.core.settings.configdb import settings

class MongoDB:
    def __init__(self):
        self.client = MongoClient(
            f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@"
            f"{settings.MONGO_SERVER}:{settings.MONGO_PORT}/"
        )
        self.db = self.client[settings.MONGO_DB]
    
    def get_collection(self, collection_name: str):
        return self.db[collection_name]
    
mongodb = MongoDB()