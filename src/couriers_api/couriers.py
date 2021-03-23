from datetime import datetime

from .database import mongo
from faker import Faker


def get_available_courier(order_id: str) -> str:
    courier = {
        "name": Faker().name(),
        "status": "assigned",
        "orders": [{"order": order_id, "timestamp": datetime.utcnow()}]
    }

    inserted_courier = mongo.db.couriers.insert_one(courier)

    return str(inserted_courier.inserted_id)
