from pymongo import MongoClient

from config import DB_URL

client = MongoClient(DB_URL)
db = client["mydb"]
collection = db["links"]
new_collection = db["new_links"]
