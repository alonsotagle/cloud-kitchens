import json

import src

from .order_factory import create_fake_order
from src.kitchen_api.database import mongo
from src.kitchen_api.shelves import is_order_in_shelf

def test_process_order(client, faker, monkeypatch):

    def mock_request_courier(order_id: str) -> None:
        return None

    monkeypatch.setattr(
        src.kitchen_api.process_order,
        "request_courier",
        mock_request_courier,
    )

    fake_order_id = faker.uuid4()

    fake_order = create_fake_order(faker, fake_order_id)

    response = client.post("/orders", json=fake_order)

    data = json.loads(response.data)

    assert response.status_code == 201
    assert isinstance(data, dict)
    assert data.get("message").find(str(fake_order_id)) != -1
    
    order = mongo.db.orders.find_one({"_id": fake_order_id})
    assert str(order.get("_id")) == fake_order_id
    assert order.get("status") == "shelf"

    assert is_order_in_shelf(fake_order_id)
