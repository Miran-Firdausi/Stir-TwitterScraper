from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from django.conf import settings


def get_db():
    client = MongoClient(settings.MONGO_URI, server_api=ServerApi("1"))
    return client["twitter-scraper"]
