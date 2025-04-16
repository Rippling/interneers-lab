import pytest
import mongoengine
from mongoengine import connect, disconnect
from products.models.ProductModel import ProductCategory, Product
from pymongo.mongo_client import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from django.conf import settings
from rest_framework.test import APIClient
from seed_data import seed_database

# Check if MongoDB is available, otherwise use mongomock
def is_mongodb_available():
    try:
        client = MongoClient(host='localhost', port=27017, serverSelectionTimeoutMS=1000)
        client.admin.command('ismaster')
        return True
    except ServerSelectionTimeoutError:
        return False

@pytest.fixture(scope="session")
def mongodb_use_local():
   
    return is_mongodb_available()

@pytest.fixture(scope="function")
def db(mongodb_use_local):

    mongoengine.disconnect_all()
    
    if mongodb_use_local:
       
        mongoengine.connect(
            db='test_products_db',
            host='localhost',
            port=27017,
            alias='default'
        )
        print("Using local MongoDB for tests")
    else:
        
        import mongomock
        mongoengine.connect(
            db='test_products_db',
            host='mongomock://localhost',
            alias='default',
            uuidRepresentation='standard'
        )
        print("Using mongomock for tests")
    
    
    seed_data = seed_database()
    
    yield seed_data
   
    mongoengine.disconnect_all()

@pytest.fixture
def api_client():
    return APIClient()