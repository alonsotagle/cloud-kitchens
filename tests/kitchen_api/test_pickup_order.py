import json


from .order_factory import create_fake_order

from src.kitchen_api.database import mongo
from src.kitchen_api.orders import insert_order
from src.kitchen_api.shelves import assign_shelf


def test_cant_pickup_order(client, faker):

    fake_order_id = faker.uuid4()
    fake_courier_id = faker.uuid4()

    response = client.post(f"/orders/{fake_order_id}/pickup", json={"courierId": fake_courier_id})

    data = json.loads(response.data)

    assert response.status_code == 400
    assert isinstance(data, dict)
    assert data.get("message").find(str(fake_order_id)) != -1


def test_pickup_order(client, faker):

    fake_order_id = faker.uuid4()
    fake_order = create_fake_order(faker, fake_order_id)
    insert_order(fake_order)
    assign_shelf(fake_order)

    fake_courier_id = faker.uuid4()

    response = client.post(f"/orders/{fake_order_id}/pickup", json={"courierId": fake_courier_id})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get("message").find(str(fake_order_id)) != -1
    assert data.get("message").find(str(fake_courier_id)) != -1

    order = mongo.db.orders.find_one({"_id": fake_order_id})
    assert order.get("status") == "delivered"
    assert order.get("courierId") == fake_courier_id
