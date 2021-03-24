import json

from src.couriers_api.database import mongo


def test_assign_courier(client, faker):

    fake_order_id = faker.uuid4()

    response = client.post("/couriers", json={"orderId": fake_order_id})

    data = json.loads(response.data)


    assert response.status_code == 200
    assert isinstance(data, dict)

    courier = mongo.db.couriers.find_one({"orders.order": fake_order_id})
    assert data.get("message").find(str(courier.get("_id"))) != -1
    assert len(courier.get("orders")) == 1
    assert courier.get("status") == "assigned"
