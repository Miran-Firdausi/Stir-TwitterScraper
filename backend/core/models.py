from datetime import datetime
from .utils import get_db

db = get_db()


class TrendingTopic:
    @staticmethod
    def save_topics(topics, ip_address):
        collection = db["trending_topics"]
        data = {
            "timestamp": datetime.utcnow(),
            "ip_address": ip_address,
            "topics": topics,
        }
        collection.insert_one(data)
        return data

    @staticmethod
    def get_latest_record():
        collection = db["trending_topics"]
        latest_record = collection.find_one(sort=[("timestamp", -1)])
        return latest_record
