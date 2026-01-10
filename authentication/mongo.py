from pymongo import MongoClient
from django.conf import settings
import os

if settings.MONGO_URI:
    # ✅ Atlas (staging / cloud)
    client = MongoClient(settings.MONGO_URI)
else:
    # ✅ Local / Server MongoDB
    client = MongoClient(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
    )

# Connect to the database
db = client["gym_management"]

# Collections
users_collections = db["Users"]
orgs_collections = db["Orgs"]
members_collections = db["Members"]
trainers_collections = db["Trainers"]
payments_collections = db["Payments"]
