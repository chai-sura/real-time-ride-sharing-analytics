import json
import logging
import time
from kafka import KafkaConsumer, errors
from pymongo import MongoClient

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Retry until MongoDB is ready
while True:
    try:
        mongo_client = MongoClient("mongodb://mongo:27017/")
        db = mongo_client["ride_analytics"]
        city_metrics_col = db["city_metrics"]
        logging.info("Connected to MongoDB!")
        break
    except Exception as e:
        logging.warning(f"MongoDB not ready, retrying in 2s... ({e})")
        time.sleep(2)

# Retry until Kafka is ready
while True:
    try:
        consumer = KafkaConsumer(
            "ride-events",
            bootstrap_servers="kafka:9092",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id="ride-processor-group"
        )
        logging.info("Connected to Kafka!")
        break
    except errors.NoBrokersAvailable:
        logging.warning("Kafka not ready, retrying in 2s...")
        time.sleep(2)

logging.info("Ride Stream Processor started. Listening to Kafka topic 'ride-events'...")

# Consume events
for message in consumer:
    event = message.value
    city = event.get("city")
    rides = event.get("rides", 1)
    revenue = event.get("revenue", 0.0)

    if not city:
        logging.warning(f"Skipped event without city: {event}")
        continue

    result = city_metrics_col.update_one(
        {"city": city},
        {"$inc": {"rides": rides, "revenue": revenue}},
        upsert=True
    )
    logging.info(f"Processed event for city '{city}': rides={rides}, revenue={revenue}")