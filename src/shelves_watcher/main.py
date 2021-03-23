import os
import requests
import time

from time import sleep

from json import dumps
from pymongo import MongoClient
    

client = MongoClient(
    host=os.environ.get("MONGODB_HOSTNAME", "localhost"),
    authSource=os.environ.get("MONGODB_DATABASE", "cloudkitchensdb"),
    username=os.environ.get("MONGODB_USERNAME", "shelves"),
    password=os.environ.get("MONGODB_PASSWORD", "HTBbK7z!N9kftjWK"),
)

db = client[os.environ.get("MONGODB_DATABASE", "cloudkitchensdb")]

def shelves_watcher():
    shelves = db.shelves.find( {} )

    for shelf in shelves:
        for shelf_order in shelf.get("orders"):
            value = calculate_value(shelf_order, shelf.get("decayModifier"))
            if value <= 0:
                remove_order(shelf.get("temperature"), shelf_order.get("id"))


def calculate_value(shelf_order: dict, shelf_decay_modifier: int) -> float:
    shelf_life = shelf_order.get("shelfLife")
    decay_rate = shelf_order.get("decayRate")
    order_age = time.time_ns() - shelf_order.get("timestamp")

    return (shelf_life - order_age - decay_rate * order_age * shelf_decay_modifier) / shelf_life


def remove_order(shelf_temperature: str, order_id: str):
    host_kitchen = os.environ.get("HOST_KITCHEN")
    requests.delete(
        f"{host_kitchen}/orders/{order_id}",
        headers={"Content-Type": "application/json"},
        data=dumps({ "shelfTemperature": shelf_temperature })
    )


while True:
    shelves_watcher()
    sleep(5)
