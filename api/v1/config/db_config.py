from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
"""
db_config module

Connect to our database and create collections
"""

uri = "mongodb://localhost:27017/"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client.nkhunda_db

# collections initialisation
app_collection = db['app']
user_collection = db['user']
message_collection = db['message']
group_collection = db['group']
chat_collection = db['chat']
organisation_collection = db['organisation']
notification_collection = db['notification']


collection = {
    "app": app_collection,
    "user": user_collection,
    "message": message_collection,
    "group": group_collection,
    "chat": chat_collection,
    "notification": notification_collection,
    "org": organisation_collection
}