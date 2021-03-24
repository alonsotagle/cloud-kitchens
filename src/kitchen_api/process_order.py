import os
import requests

from json import dumps

from .orders import insert_order, log_order_status
from .shelves import assign_shelf


def process_order(order: dict) -> dict:
    order_id = insert_order(order)

    log_order_status(order_id, "received")
    log_order_status(order_id, "preparing")

    assign_shelf(order)
    log_order_status(order_id, "shelf")

    request_courier(order_id)

    return {"message": f"Processing order {order_id}"}, 201


def request_courier(order_id: str) -> None:
    host_couriers = os.environ.get("HOST_COURIERS")
    requests.post(f"{host_couriers}/couriers", headers={"Content-Type": "application/json"}, data=dumps({"orderId": order_id}))
