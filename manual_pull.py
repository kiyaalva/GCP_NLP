from google.cloud import pubsub_v1

project_id = "careful-synapse-461801-f6"
subscription_id = "news-headlines-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

print(f"📡 Pulling messages from {subscription_path}...")

response = subscriber.pull(
    request={
        "subscription": subscription_path,
        "max_messages": 10,
    },
    timeout=10,
)

if not response.received_messages:
    print("❌ No messages found.")
else:
    for msg in response.received_messages:
        print(f"📰 Received: {msg.message.data.decode('utf-8')}")
        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [msg.ack_id],
            }
        )
        print("✅ Message acknowledged.")
