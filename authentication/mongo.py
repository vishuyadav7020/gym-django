from pymongo import MongoClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

if settings.MONGO_URI:
    logger.info("✅ Connecting to MongoDB ATLAS")
    client = MongoClient(settings.MONGO_URI)
else:
    logger.info(
        f"✅ Connecting to LOCAL MongoDB at {settings.MONGO_HOST}:{settings.MONGO_PORT}"
    )
    client = MongoClient(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
    )
# Connect to the database
db = client["gym_management"]
logger.info("✅ MongoDB connection initialized")
# Collections
users_collections = db["Users"]
orgs_collections = db["Orgs"]
members_collections = db["Members"]
trainers_collections = db["Trainers"]
payments_collections = db["Payments"]
