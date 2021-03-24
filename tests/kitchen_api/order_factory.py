from faker import Faker

def create_fake_order(faker: Faker, fake_order_id: str) -> dict:
    return {
        "id": fake_order_id,
        "name":faker.word(),
        "temp": faker.random_element(["hot", "cold", "frozen"]),
        "shelfLife": faker.pyint(),
        "decayRate": faker.pyfloat(positive=True, max_value=1.0, right_digits=2)
    }
