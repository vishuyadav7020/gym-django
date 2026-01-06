from pymongo import MongoClient
from django.conf import settings

client = MongoClient(
    host=settings.MONGO_HOST,
    port=settings.MONGO_PORT,
)

db = client["gym_management"]

users_collections = db["Users"]
orgs_collections = db["Orgs"]
members_collections = db["Members"]
trainers_collections = db["Trainers"]
payments_collections = db["Payments"]
