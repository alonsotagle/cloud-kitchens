# cloud-kitchens

## PREREQUISITES

- [Docker](https://docs.docker.com/get-docker/)

## RUN

1. Run command `make build` to run kafka server

![make build](https://cloudkitchens.s3-us-west-2.amazonaws.com/build.gif)

2. Run command `make start` to run kafka producer and kafka consumer, MongoDB database, microservices and daemon, you will see logs of order statuses

![make start](https://cloudkitchens.s3-us-west-2.amazonaws.com/start.gif)

To configure the order ingestion change the variables `DELAY_TIME` and `BATCH_SIZE` in `infra/docker-compose.start.yml`

## TESTS

Command to run tests:

```sh
make run-tests
```

![make run-tests](https://cloudkitchens.s3-us-west-2.amazonaws.com/tests.gif)


## ARCHITECTURE

| Name              | Path                  | Container             | Tech                          |
|-------------------|-----------------------|-----------------------|-------------------------------|
| Zookeper          | -                     | zookeper              | Zookeper                      |
| Kafka             | -                     | kafka                 | Kafka                         |
| MongoDB           | -                     | mongodb               | MongoDB                       |
| Couriers API      | src/couriers_api/     | couriers              | Flask, PyMongo                |
| Shelves watcher   | src/shelves_watcher/  | shelves_watcher       | PyMongo                       |
| Kitchen API       | src/kitchen_api/      | kitchen               | Flask, PyMongo                |
| Orders consumer   | src/orders_consumer/  | orders_consumer       | kafka-python, KafkaConsumer   |
| Orders producer   | src/orders_producer/  | orders_producer       | kafka-python, KafkaProducer   |
| MongoDB test      | -                     | mongodb_test          | MongoDB                       |
| Tests             | tests/                | tests                 | Pytest                        |

TODO Diagram

## CHALLENGE TASKS

[x] Orders must be parsed from the file and ingested into your system

[x] The kitchen should receive 2 delivery orders per second

[x] It's expected to make your order ingestion rate configurable

[x] The kitchen should instantly cook the order

[x] The system should dispatch a courier to pick up and deliver that ​specific​ order

[x] Each order should only be ingested once

[x] Each order should be placed on a shelf that matches the order’s temperature

[x] If that shelf is full, an order can be placed on the overflow shelf

[x] If the overflow shelf is full, an existing order of your choosing on the overflow should be moved to an allowable shelf with room​.​ If no such move is possible, a random order from the overflow shelf should be discarded as waste

[x] Orders that have reached a value of zero are considered wasted: they should never be delivered and should be removed from the shelf

[x] Please display the current order value when displaying an order in your system’s output


## ENDPOINTS

### Kitchen API

```
POST /orders
{
    "id": "string",
    "name": "string",
    "temp": "string",
    "shelfLife": 1,
    "decayRate": 1.0
}


POST /orders/<string:order_id>/pickup
{"courierId": "string"}


DELETE /orders/<string:order_id>
{"shelfTemperature": "string"}
```

### Couriers API

```
POST /couriers
{"orderId": "string"}
```

## DATA STRUCTURES

### Orders
```json
{
    "_id": "a8cfcb76-7f24-4420-a5ba-d46dd77bdffd",
    "courierId": "605c3f0d6e75ee19eefd9bda",
    "decayRate": 0.63,
    "logs": [
        {
        "status": "received",
        "timestamp": {"$date": "2021-03-25T07:43:09.480Z"}
        },
        {
        "status": "preparing",
        "timestamp": {"$date": "2021-03-25T07:43:09.485Z"}
        },
        {
        "status": "shelf",
        "timestamp": {"$date": "2021-03-25T07:43:09.511Z"}
        },
        {
        "status": "courier",
        "timestamp": {"$date": "2021-03-25T07:43:14.173Z"}
        },
        {
        "status": "delivered",
        "timestamp": {"$date": "2021-03-25T07:43:14.251Z"}
        }
    ],
    "name": "Banana Split",
    "shelf": "frozen",
    "shelfLife": 20,
    "status": "delivered",
    "temp": "frozen"
}
```

### Shelves
```json
{
    "_id": {"$oid": "605c41ce4f641185af9e8a58"},
    "capacity": 10,
    "decayModifier": 1,
    "name": "Hot shelf",
    "orders": [
        {
        "id": "dcafe7ca-f7a7-4262-9b14-ab19729b2055",
        "shelfLife": 201,
        "decayRate": 0.74,
        "temperature": "hot",
        "timestamp": 1616658913343715600
        },
        {
        "id": "d2d2d948-f019-4806-bb7e-bb2172bd75d9",
        "shelfLife": 200,
        "decayRate": 0.63,
        "temperature": "hot",
        "timestamp": 1616658914058507700
        },
        {
        "id": "8275f014-ed83-4554-b0ff-0dbdc24e57ad",
        "shelfLife": 220,
        "decayRate": 0.67,
        "temperature": "hot",
        "timestamp": 1616658914481311200
        },
        {
        "id": "e537a1b8-1505-49ae-a71e-a3ab80e8b606",
        "shelfLife": 222,
        "decayRate": 0.71,
        "temperature": "hot",
        "timestamp": 1616658915038003100
        }
    ],
    "temperature": "hot"
}
```

### Couriers
```json
{
    "_id": {"$oid": "605c3f0d6e75ee19eefd9bda"},
    "name": "David Bender",
    "orders": [
        {
        "order": "a8cfcb76-7f24-4420-a5ba-d46dd77bdffd",
        "timestamp": {"$date": "2021-03-25T07:43:09.780Z"}
        }
    ],
    "status": "assigned"
}
```

## MONGO
### User for reporting

```
host
localhost:27017/cloudkitchensdb

user
reporting

password
Ic^s38cIy%L^mA83
```

### Queries while running

db.orders.find();
![db_orders](https://cloudkitchens.s3-us-west-2.amazonaws.com/db_orders.gif)

db.shelves.find();
![db_shelves](https://cloudkitchens.s3-us-west-2.amazonaws.com/db_shelves.gif)

db.couriers.find();
![db_couriers](https://cloudkitchens.s3-us-west-2.amazonaws.com/db_couriers.gif)
