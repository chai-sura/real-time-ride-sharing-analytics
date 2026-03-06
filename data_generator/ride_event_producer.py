from kafka import KafkaProducer, errors
import json
from faker import Faker
import time

fake = Faker()

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        break
    except errors.NoBrokersAvailable:
        print("Kafka not ready, retrying in 2 seconds...")
        time.sleep(2)

while True:
    ride_event = {
        "city": fake.city(),
        "rides": fake.random_int(min=1, max=10),
        "revenue": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)
    }
    producer.send('ride-events', ride_event)
    print(f"Produced ride event: {ride_event}")
    time.sleep(1)