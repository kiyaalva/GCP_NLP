import requests
from google.cloud import pubsub_v1
import time
import json

# 🔧 CONFIG
with open("config.json") as f:
    config = json.load(f)

API_KEY = config["api_key"]
country = config["country"]
project_id = config["project_id"]
topic_id = config["topic_id"]


# 🔌 Pub/Sub setup
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def fetch_headlines():
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ NewsAPI Error:", response.status_code, response.text)
        return []
    data = response.json()
    headlines = [article["title"] for article in data["articles"] if article["title"]]
    return headlines

def publish_headlines(headlines):
    for headline in headlines:
        data = headline.encode("utf-8")
        future = publisher.publish(topic_path, data=data)
        print(f"✅ Published: {headline} (msg ID: {future.result()})")

if __name__ == "__main__":
    print("🚀 Streaming headlines to Pub/Sub...")
    headlines = fetch_headlines()
    publish_headlines(headlines)