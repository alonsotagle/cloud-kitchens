import pytest


@pytest.fixture
def client():
    from src.couriers_api.main import app
    return app.test_client()


@pytest.fixture
def faker():
    from faker import Faker

    return Faker()
