import os
import requests

from json import loads, dumps

from kafka import KafkaConsumer


consumer = KafkaConsumer(
    os.environ.get("KAFKA_TOPIC_ORDERS", "orders"),
    bootstrap_servers=os.environ.get("KAFKA_SERVER", "localhost:9092"),
    group_id=None,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: loads(m.decode("utf-8")),
    api_version=(0, 11, 5)
)


for event in consumer:
    event_data = event.value

    host_kitchen = os.environ.get("HOST_KITCHEN")
    requests.post(
        f"{host_kitchen}/orders",
        headers={"Content-Type": "application/json"},
        data=dumps(event_data)
    )
