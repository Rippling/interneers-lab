import pytest
import mongoengine
import os
from product.scripts.seed_testDB import seed_test_database,clear_test_data

#creates conn. to a MOongoDB test db for entire test session
@pytest.fixture(scope="session")
def mongodb_connection():
    test_db_host=os.environ.get('TEST_MONGODB_HOST', 'localhost')
    test_db_port=int(os.environ.get('TEST_MONGODB_PORT', 27017))
    test_db_name=os.environ.get('TEST_MONGODB_NAME', 'test_product_db')
    
    connection=mongoengine.connect(
        db=test_db_name,
        host=test_db_host,
        port=test_db_port,
        alias='default'
    )
    yield connection
    mongoengine.disconnect(alias='default')

#seed test MONGODB with categ. and prod for each test
@pytest.fixture(scope="function")
def test_data(mongodb_connection):
    data=seed_test_database()
    yield data
    clear_test_data()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()