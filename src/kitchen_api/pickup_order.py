from flask import current_app as app

from .orders import log_order_status, assign_order_courier
from .shelves import remove_shelf_order, is_order_in_shelf

def pickup_order(order_id: str, courier_id: str) -> dict:

    if not is_order_in_shelf(order_id):
        return {"message": f"Order {order_id} wasted"}, 400

    app.logger.info(f"Order {order_id} - courier {courier_id}")

    log_order_status(order_id, "courier")

    assign_order_courier(order_id, courier_id)

    remove_shelf_order(order_id)

    log_order_status(order_id, "delivered")

    return {"message": f"Order {order_id} collected by {courier_id}"}
