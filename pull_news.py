from google.cloud import pubsub_v1
from google.cloud import bigquery
from textblob import TextBlob
from datetime import datetime
import time
import json
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# 🔧 CONFIG
with open("config.json") as f:
    config = json.load(f)


project_id = config["project_id"]
topic_id = config["topic_id"]
subscription_id = config["subscription_id"]
dataset_id = config["dataset_id"]
table_id = config["table_id"]

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# BigQuery setup
bq_client = bigquery.Client()
table_ref = bq_client.dataset(dataset_id).table(table_id)

# Sentiment scoring
analyzer = SentimentIntensityAnalyzer()

# New sentiment function using VADER
def get_sentiment(text):
    score = analyzer.polarity_scores(text)["compound"]
    if score > 0.2:
        return "Positive"
    elif score < -0.2:
        return "Negative"
    else:
        return "Neutral"


# Message handler
def callback(message):
    headline = message.data.decode("utf-8")
    sentiment = get_sentiment(headline)
    timestamp = datetime.utcnow()

    print(f"📰 {headline} → 🧠 {sentiment}")

    row = [{
        "headline": headline,
        "sentiment": sentiment,
        "published_at": timestamp.isoformat()
    }]

    errors = bq_client.insert_rows_json(table_ref, row)
    if errors:
        print("❌ Failed to insert:", errors)
    else:
        print("✅ Inserted into BigQuery")

    message.ack()

# Start subscriber
print("🚀 Listening to Pub/Sub for 60 seconds...")
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    time.sleep(60)
    streaming_pull_future.cancel()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("⏹️ Stopped.")

score_obj = analyzer.polarity_scores(text)
print(f"🔍 VADER Score: {score_obj}")