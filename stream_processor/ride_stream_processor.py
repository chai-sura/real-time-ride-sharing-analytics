import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from collections import defaultdict

consumer = KafkaConsumer(
    "ride_events",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

client = MongoClient("mongodb://localhost:27017/")
db = client["ride_analytics"]
collection = db["city_metrics"]

city_stats = defaultdict(lambda: {"rides": 0, "revenue": 0})

for message in consumer:
    event = message.value
    city = event["city"]

    city_stats[city]["rides"] += 1
    city_stats[city]["revenue"] += event["fare"]

    collection.update_one(
        {"city": city},
        {"$set": city_stats[city]},
        upsert=True
    )

    print("Processed:", city, city_stats[city])