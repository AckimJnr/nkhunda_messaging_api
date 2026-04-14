"""
db_config module

Connect to MongoDB and expose named collection references.
All configuration is loaded from environment variables via settings.
"""

from pymongo.mongo_client import MongoClient
from config.settings import settings

# Create a single client and connect to the server
client = MongoClient(settings.MONGO_URI)

db = client[settings.DB_NAME]

# Collection references
app_collection = db["app"]
user_collection = db["user"]
message_collection = db["message"]
group_collection = db["group"]
chat_collection = db["chat"]
organisation_collection = db["organisation"]
notification_collection = db["notification"]

collection = {
    "app": app_collection,
    "user": user_collection,
    "message": message_collection,
    "group": group_collection,
    "chat": chat_collection,
    "notification": notification_collection,
    "org": organisation_collection,
}