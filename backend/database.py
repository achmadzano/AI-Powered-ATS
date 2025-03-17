from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Koneksi ke MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["ats_database"]

# Collection untuk role & CV
roles_collection = db["roles"]
cv_collection = db["cvs"]

# Cek koneksi
try:
    client.admin.command("ping")
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print("MongoDB connection failed:", e)
