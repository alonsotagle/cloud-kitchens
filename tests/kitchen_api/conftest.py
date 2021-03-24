import pytest

from src.kitchen_api.main import app, initialize_db


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def faker():
    from faker import Faker

    return Faker()


@pytest.fixture
def app_context():
    testing_client = app.test_request_context()
    testing_client.push()
    yield app
    testing_client.pop()


@pytest.fixture(autouse=True)
def reset_db(app_context):
    with app_context.app_context():
        initialize_db()
