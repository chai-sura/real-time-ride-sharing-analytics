from kafka import KafkaProducer, errors
import json
from faker import Faker
import time

fake = Faker()

# Retry until Kafka is ready
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",  # must match the service name in docker-compose
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print("Connected to Kafka!")
        break
    except errors.NoBrokersAvailable:
        print("Kafka not ready, waiting 2 seconds...")
        time.sleep(2)

while True:
    event = {
        "city": fake.city(),
        "rides": fake.random_int(1, 10),
        "revenue": round(fake.pyfloat(left_digits=2, right_digits=2), 2)
    }
    producer.send("ride-events", value=event)
    producer.flush()
    print("Produced event:", event)
    time.sleep(1)