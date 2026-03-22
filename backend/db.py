from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variable
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGODB_URI)

db = client["fact_checker"]
collection = db["facts"]
