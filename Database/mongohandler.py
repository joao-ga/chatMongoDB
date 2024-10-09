import pymongo
from pymongo import MongoClient
#import scikit-learn
from Database.entities import Message


class Operation:
    def __init__(self):
        self.connection_string = "mongodb+srv://jbiazonferreira:123456qwerty@aulas.joxwh.mongodb.net/?retryWrites=true&w=majority&appName=aulas"
        self.client = MongoClient(self.connection_string)
        self.db = self.client["chatMongo"]
        self.users_collection = self.db.users
        self.messages_collection = self.db.messages

    def add_new_message(self, m: Message):
        return self.messages_collection.insert_one(m.to_dict()).inserted_id

    def find_user(self, email: str, password: str):
        user = self.users_collection.find_one({"email": email}, {"password": password})

        if user is not None:
            return True
        else:
            return False

