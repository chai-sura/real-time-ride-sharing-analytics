import json
import time
import random
from kafka import KafkaProducer
from faker import Faker

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

cities = ["San Francisco", "New York", "Chicago", "Seattle", "Austin"]

def generate_event():
    return {
        "ride_id": fake.uuid4(),
        "driver_id": random.randint(1000, 2000),
        "city": random.choice(cities),
        "distance_km": round(random.uniform(1, 20), 2),
        "fare": round(random.uniform(5, 60), 2),
        "timestamp": time.time()
    }

while True:
    event = generate_event()
    producer.send("ride_events", event)
    print("Produced:", event)
    time.sleep(0.1)