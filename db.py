from pymongo import MongoClient
from dotenv import dotenv_values
config = dotenv_values(".env")

CONNECTION_STRING = config["MONGO_URI"] + "&uuidRepresentation=standard"
client = MongoClient(CONNECTION_STRING)
print("created new client")
db = client[config["dbName"]]
users = db["users"]
usersCreds = db["credentials"]
