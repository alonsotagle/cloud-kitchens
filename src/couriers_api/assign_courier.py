import os
import requests

from json import dumps
from multiprocessing import Process
from random import randint
from time import sleep

from .couriers import get_available_courier


def assign_courier(data) -> dict:
    order_id = data.get("orderId")

    courier_id = get_available_courier(order_id)

    async_pickup(order_id, courier_id)

    return {"message": f"Sending courier {courier_id}"}


def async_pickup(order_id: str, courier_id: str) -> None:
    async_process = Process(
        target=confirm_pickup,
        args=(order_id, courier_id),
        daemon=True
    )
    async_process.start()


def confirm_pickup(order_id: str, courier_id: str) -> None:
    delay = randint(2, 6)
    sleep(delay)

    host_kitchen = os.environ.get("HOST_KITCHEN")
    requests.post(
        f"{host_kitchen}/orders/{order_id}/pickup",
        headers={"Content-Type": "application/json"},
        data=dumps({"courierId": courier_id})
    )
