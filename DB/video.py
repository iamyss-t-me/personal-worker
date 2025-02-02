from pymongo import MongoClient
from typing import Optional
from pydantic import BaseModel
from config import Config

class Screenshot(BaseModel):
    id: int
    url: str
    timestamp: str

class Video(BaseModel):
    id: str
    title: str
    telegramid: int
    size: float
    views: int = 0
    likes: int = 0
    dislikes: int = 0
    screenshots: Optional[list[Screenshot]] = None
    

class DB:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client["project1"]
        self.collection = self.db["videos"]

    def add_video(self, video: Video):
        self.collection.insert_one(video.model_dump())

    def get_video(self, id: str) -> Video:
       return Video(**self.collection.find_one({"id": id}))  if self.collection.find_one({"id": id}) else None
    
    def get_videos(self) -> list[Video]:
        return [Video(**video) for video in self.collection.find()]
    
    def update_video(self, id: str, video: Video):
        self.collection.update_one({"id": id}, {"$set": video.model_dump()})

class Admin:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client["project1"]
        self.collection = self.db["admin"]
    def get_admins(self):
        pass
