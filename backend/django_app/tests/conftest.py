import pytest
from rest_framework.test import APIClient
from django_app.scripts.seed_data import seed_categories, seed_products

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def seeded_data(db):
    categories = seed_categories()
    seed_products(categories)
    return categories
