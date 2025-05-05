import pytest
from rest_framework.test import APIClient
from products.models import Product, Category
from products.tests.utils import api_client, sample_category, sample_product, teardown_data

@pytest.mark.integration
def test_create_and_get_product(db):
    client = APIClient()
    # Create a category first
    category = Category(name="IntegrationCat").save()
    
    # Create a product
    product_data = {
        "sku": "INT-12345",
        "name": "Integration Product",
        "description": "Created by integration test",
        "category": str(category.id),
        "brand": "TestBrand",
        "tags": ["integration", "test"],
        "price": 99.99,
        "quantity": 10,
        "dimensions": "10x10x10"
    }
    response = client.post("/api/products/", product_data, format="json")
    assert response.status_code == 201
    slug = response.data["slug"]

    # Fetch the product by slug
    response = client.get(f"/api/products/{slug}/")
    assert response.status_code == 200
    assert response.data["name"] == "Integration Product"
    assert response.data["sku"] == "INT-12345"
    
    # Clean up
    Product.objects.delete()
    Category.objects.delete() 