import os

from flask import Flask, request

from .database import mongo
from .process_order import process_order
from .pickup_order import pickup_order
from .discard_order import discard_order


app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{os.environ.get('MONGODB_USERNAME')}:{os.environ.get('MONGODB_PASSWORD')}@{os.environ.get('MONGODB_HOSTNAME')}:27017/{os.environ.get('MONGODB_DATABASE')}"
mongo.init_app(app)


@app.before_first_request
def initialize_db() -> None:
    mongo.db.orders.drop()
    mongo.db.shelves.drop()
    mongo.db.couriers.drop()

    mongo.db.shelves.insert_many([
        { "name": "Hot shelf", "temperature": "hot", "capacity": 10, "orders": [], "decayModifier": 1 },
        { "name": "Cold shelf", "temperature": "cold", "capacity": 10, "orders": [], "decayModifier": 1 },
        { "name": "Frozen shelf", "temperature": "frozen", "capacity": 10, "orders": [], "decayModifier": 1 },
        { "name": "Overflow shelf", "temperature": "overflow", "capacity": 15, "orders": [], "decayModifier": 2 },
    ])


@app.route("/orders", methods=["POST"])
def process():
    return process_order(request.get_json())


@app.route("/orders/<string:order_id>/pickup", methods=["POST"])
def pickup(order_id):
    return pickup_order(order_id, request.get_json().get("courierId"))


@app.route("/orders/<string:order_id>", methods=["DELETE"])
def discard(order_id):
    return discard_order(request.get_json().get("shelfTemperature"), order_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
