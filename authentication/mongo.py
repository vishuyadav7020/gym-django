from pymongo import MongoClient
from django.conf import settings
import logging, os
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

##Uncomment when using not using Docker Conatiner
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

##Comment it When not Using Kubernates
# MONGO_URI = os.getenv("MONGO_URI")
# if not MONGO_URI:
#     raise RuntimeError("MONGO_URI must be set")

# logger.info("✅ Connecting to MongoDB via MONGO_URI")
# client = MongoClient(MONGO_URI)

# parsed = urlparse(MONGO_URI)
# db_name = parsed.path.lstrip("/")

# db = client[db_name]
# logger.info(f"✅ MongoDB connection initialized (DB: {db_name})")


##Remains Same Both Ways
# Connect to the database
db = client["gym_management"]
logger.info("✅ MongoDB connection initialized")
# Collections
users_collections = db["Users"]
orgs_collections = db["Orgs"]
members_collections = db["Members"]
trainers_collections = db["Trainers"]
payments_collections = db["Payments"]