import os

from flask import Flask, request

from .database import mongo
from .assign_courier import assign_courier

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{os.environ.get('MONGODB_USERNAME')}:{os.environ.get('MONGODB_PASSWORD')}@{os.environ.get('MONGODB_HOSTNAME')}:{os.environ.get('MONGODB_PORT')}/{os.environ.get('MONGODB_DATABASE')}"
mongo.init_app(app)

@app.route("/couriers", methods=["POST"])
def assign():
    return assign_courier(request.get_json())


if __name__ == "__main__":
    app.run(host="0.0.0.0")
