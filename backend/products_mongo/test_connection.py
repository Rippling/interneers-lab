import os
from dotenv import load_dotenv
from mongoengine import connect
from pymongo import MongoClient

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB using MongoEngine
def init_db():
    connect(host=MONGO_URI, alias="default")

