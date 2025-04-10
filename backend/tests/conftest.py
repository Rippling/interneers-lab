import pytest
from mongoengine import connect, disconnect
from tests.seed_data.clear_database import clear_database

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    disconnect(alias="default")
    connect("test_db", host="mongodb://localhost:27017/test_db", alias="default")
    
    yield
    
    clear_database()
    disconnect()

@pytest.fixture(autouse=True)
def reset_db():
    clear_database()
