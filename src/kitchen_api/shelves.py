import time

from flask import current_app as app

from .database import mongo
from .orders import log_order_status

def assign_shelf(order: dict) -> None:
    temperature = order.get("temp")
    order_id = order.get("_id")

    shelf_temperature = get_available_shelf(temperature)

    data = {
        "id": order_id,
        "shelfLife": order.get("shelfLife"),
        "decayRate": order.get("decayRate"),
        "temperature": order.get("temp"),
        "timestamp": time.time_ns()
    }

    push_order(shelf_temperature, data)

    save_order_shelf(order_id, shelf_temperature)


def get_available_shelf(temperature: str) -> str:

    shelf = get_shelf_by_temperature(temperature)

    if not can_place_order(shelf):
        if temperature == "overflow":
            orders = shelf.get("orders")
            if not can_free_overflow(orders):
                order_id = orders.pop().get("id")
                set_order_to_waste("overflow", order_id)
                return "overflow"
        return get_available_shelf("overflow")

    return shelf.get("temperature")


def push_order(shelf_temperature: str, data: dict) -> None:
    mongo.db.shelves.update_one(
        {"temperature": shelf_temperature},
        {"$push": { "orders": data }}
    )


def get_shelf_by_temperature(temperature: str) -> dict:
    return mongo.db.shelves.find_one({"temperature": temperature})


def can_place_order(shelf: dict) -> bool:
    return len(shelf.get("orders")) < shelf.get("capacity")


def can_free_overflow(orders: list) -> bool:
    shelves = {}
    for order in orders:
        shelves.setdefault(order.get("temperature"), []).append(order)

    for shelf_temperature, orders in shelves.items():
        shelf = get_shelf_by_temperature(shelf_temperature)
        if can_place_order(shelf):
            order = orders.pop()
            pull_order(shelf_temperature, order.get("id"))
            push_order(shelf_temperature, order)
            return True
    return False


def save_order_shelf(order_id: str, shelf_name: str) -> None:
    mongo.db.orders.update_one(
        {"_id": order_id},
        {
            "$set": {"shelf": shelf_name}
        }
    )


def remove_shelf_order(order_id: str) -> None:
    order = mongo.db.orders.find_one({"_id": order_id})
    pull_order(order.get("shelf"), order_id)


def pull_order(shelf_temperature: str, order_id: str) -> None:
    mongo.db.shelves.update_one(
        { "temperature": shelf_temperature },
        {
            "$pull": { "orders": { "id": order_id } }
        }
    )


def set_order_to_waste(shelf_temperature: str, order_id: str) -> None:
    app.logger.info(f"Order {order_id} wasted")
    if is_order_in_shelf(order_id):
        log_order_status(order_id, "waste")
        pull_order(shelf_temperature, order_id)


def is_order_in_shelf(order_id: str) -> bool:
    return mongo.db.shelves.count_documents({ "orders.id": order_id }) > 0
