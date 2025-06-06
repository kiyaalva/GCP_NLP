from google.cloud import pubsub_v1

project_id = "careful-synapse-461801-f6"  
topic_id = "news-headlines"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

news_headlines = [
    "Breaking: AI beats humans at reasoning",
    "Stocks rise after tech rally",
    "Weather alert: Storms expected tomorrow"
]

for headline in news_headlines:
    data = headline.encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print(f"Published message ID: {future.result()}")