from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import scrape_twitter_trending


@api_view(["GET"])
def get_trending_data(request: HttpRequest):
    latest_record = scrape_twitter_trending()

    # Format response
    timestamp = latest_record["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    ip_address = latest_record["ip_address"]
    topics = [topic["name"] for topic in latest_record["topics"]]

    scraped_data = {
        "_id": str(latest_record["_id"]),
        "timestamp": timestamp,
        "ip_address": ip_address,
        "topics": topics,
    }

    return Response(scraped_data)
