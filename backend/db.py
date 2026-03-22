from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variable
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    # Try to verify connection immediately
    client.admin.command('ping')
    db = client["fact_checker"]
    collection = db["facts"]
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"⚠️  MongoDB connection failed: {e}")
    client = None
    db = None
    collection = None

