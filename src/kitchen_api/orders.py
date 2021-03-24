from datetime import datetime

from .database import mongo


def insert_order(order: dict) -> str:
    order["_id"] = order.pop("id")
    order["status"] = "created"
    order["logs"] = []
    inserted_order = mongo.db.orders.insert_one(order)
    return inserted_order.inserted_id


def log_order_status(order_id: str, status: str) -> None:
    mongo.db.orders.update_one(
        {"_id": order_id},
        {
            "$set": {"status": status},
            "$push": { "logs": { "status": status, "timestamp": datetime.utcnow() } },
        }
    )


def assign_order_courier(order_id: str, courier_id: str) -> None:
    mongo.db.orders.update_one(
        {"_id": order_id},
        {
            "$set": {"courierId": courier_id}
        }
    )
