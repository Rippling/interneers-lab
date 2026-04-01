import pytest
from pymongo import MongoClient
from mongoengine import disconnect, connect

@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient("mongodb://root:example@localhost:27019/?authSource=admin")
    yield client
    client.close()

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    disconnect()
    connect(
        db="test_db",
        host="mongodb://root:example@localhost:27019/test_db?authSource=admin"
    )
    yield
    disconnect()


@pytest.fixture(scope="function")
def test_db(mongo_client):
    db = mongo_client["test_db"]

    for collection in db.list_collection_names():
        db[collection].delete_many({})
        
    yield db

    for collection in db.list_collection_names():
        db[collection].delete_many({})

@pytest.fixture
def seeded_categories(test_db):
    from products.models import Category

    cat1 = Category(name="Fruits", description="Fresh fruits").save()
    cat2 = Category(name="Vegetables", description="Fresh vegetables").save()

    return [str(cat1.id), str(cat2.id)]

from products.models import Product

@pytest.fixture
def seeded_products(seeded_categories):
    p1 = Product(
        name="Apple",
        price=10,
        category=str(seeded_categories[0]),
        brand="Fruit Brand",
        quantity=50
    ).save()

    p2 = Product(
        name="Carrot",
        price=8,
        category=str(seeded_categories[1]),
        brand="Veg Brand",
        quantity=40
    ).save()

    return [p1.id, p2.id]


   