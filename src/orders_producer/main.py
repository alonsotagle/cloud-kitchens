import os

from json import dumps, load
from time import sleep

from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=os.environ.get("KAFKA_SERVER"),
    value_serializer=lambda x: dumps(x).encode("utf-8"),
    api_version=(0, 11, 5)
)


with open("orders.json") as orders_file:
# with open("orders.json") as orders_file:
    orders = load(orders_file)
    for idx, order in enumerate(orders):

        print(order)

        producer.send(
            os.environ.get("KAFKA_TOPIC_ORDERS"),
            value=order
        )


        if idx % int(os.environ.get("BATCH_SIZE")) == 0:
            sleep(int(os.environ.get("DELAY_TIME")))

producer.flush()
