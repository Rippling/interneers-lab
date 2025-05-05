import pytest
from rest_framework.test import APIClient
from ..models import Category, Product
from datetime import datetime
import uuid

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_category_data():
    return {
        'name': 'Test Category',
        'description': 'Test category description'
    }

@pytest.fixture
def sample_product_data(sample_category_data):
    # First create a category
    category = Category(**sample_category_data)
    category.save()
    
    return {
        'sku': 'TST-12345',
        'name': 'Test Product',
        'description': 'Test product description',
        'category': category,
        'brand': 'Test Brand',
        'tags': ['test', 'sample'],
        'price': 19.99,
        'quantity': 10,
        'low_stock_threshold': 5,
        'dimensions': '10x20x30',
        'status': 'active',
        'featured': False
    }

@pytest.fixture
def sample_category(sample_category_data):
    category = Category(**sample_category_data)
    category.save()
    return category

@pytest.fixture
def sample_product(sample_product_data):
    product = Product(**sample_product_data)
    product.save()
    return product

def teardown_data():
    """Delete all products and categories after tests"""
    Product.objects.delete()
    Category.objects.delete()

def mock_category(**kwargs):
    """Create a mock Category instance"""
    data = {
        'id': str(uuid.uuid4()),
        'name': 'Mock Category',
        'slug': 'mock-category',
        'description': 'Mock category description',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    data.update(kwargs)
    
    class MockCategory:
        def __init__(self, **attrs):
            for key, value in attrs.items():
                setattr(self, key, value)
                
        def delete(self):
            pass
            
        def save(self):
            pass
    
    return MockCategory(**data)

def mock_product(**kwargs):
    """Create a mock Product instance"""
    data = {
        'id': str(uuid.uuid4()),
        'uuid': uuid.uuid4(),
        'sku': 'TST-12345',
        'name': 'Mock Product',
        'slug': 'mock-product',
        'description': 'Mock product description',
        'category': mock_category(),
        'brand': 'Mock Brand',
        'tags': ['mock', 'test'],
        'price': 29.99,
        'discount_price': None,
        'quantity': 15,
        'low_stock_threshold': 5,
        'weight': None,
        'dimensions': '10x20x30',
        'status': 'active',
        'featured': False,
        'rating': None,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    data.update(kwargs)
    
    class MockProduct:
        def __init__(self, **attrs):
            for key, value in attrs.items():
                setattr(self, key, value)
                
        @property
        def is_in_stock(self):
            return self.quantity > 0
            
        @property
        def is_low_stock(self):
            return 0 < self.quantity <= self.low_stock_threshold
            
        def delete(self):
            pass
            
        def save(self):
            pass
    
    return MockProduct(**data) 