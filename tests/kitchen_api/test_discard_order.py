import json

from .order_factory import create_fake_order

from src.kitchen_api.database import mongo
from src.kitchen_api.orders import insert_order
from src.kitchen_api.shelves import assign_shelf


def test_discard_order(client, faker):

    fake_order_id = faker.uuid4()
    fake_order = create_fake_order(faker, fake_order_id)

    insert_order(fake_order)    
    assign_shelf(fake_order)    

    response = client.delete(f"/orders/{fake_order_id}", json={"shelfTemperature": fake_order.get("temp")})

    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data.get("message").find(str(fake_order_id)) != -1
