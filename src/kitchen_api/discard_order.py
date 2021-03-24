from .shelves import set_order_to_waste


def discard_order(shelf_temperature: str, order_id: str) -> dict:
    set_order_to_waste(shelf_temperature, order_id)
    return {"message": f"Order {order_id} wasted"}
