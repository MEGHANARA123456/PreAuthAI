from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in .env")

if not DB_NAME:
    raise RuntimeError("MONGO_DB is not set in .env")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users_collection = db["users"]
pa_collection = db["performance_appraisals"]