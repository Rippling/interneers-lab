import pytest
from rest_framework.test import APIClient
import os
os.environ["ENV"] = "test"

@pytest.fixture
def api_client():
    return APIClient()

def test_create_category(api_client):
    payload = {
        "category_name": "Test Electronics",
        "description": "Electronic devices and gadgets"
    }
    response = api_client.post("/products/categories/", payload, format="json")
    assert response.status_code == 201
    assert response.data["category_name"] == "Test Electronics"
    assert "id" in response.data

def test_create_product(api_client):
    category_response = api_client.post("/products/categories/", {
        "category_name": "Books",
        "description": "All kinds of books"
    }, format="json")
    category_id = category_response.data["id"]

    product_payload = {
        "name": "The Alchemist",
        "brand": "Penguin",
        "price_in_RS": 500,
        "quantity": 10,
        "manufacture_date": "2024-01-01",
        "expiry_date": "2026-01-01",
        "category": [category_id]
    }

    response = api_client.post("/products/", product_payload, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "The Alchemist"
    assert response.data["brand"] == "Penguin"
    assert response.data["category"] == ["Books"]

def test_create_product_with_invalid_data(api_client):
    category_response = api_client.post("/products/categories/", {
        "category_name": "Test Invalid",
        "description": "For invalid tests"
    }, format="json")
    category_id = category_response.data["id"]

    product_payload = {
        "name": "Invalid Product",
        "brand": "Test",
        "price_in_RS": -100,
        "quantity": 10,
        "manufacture_date": "2024-01-01",
        "expiry_date": "2026-01-01",
        "category": [category_id]
    }
    response = api_client.post("/products/", product_payload, format="json")
    assert response.status_code == 400
    assert "Price cannot be negative" in response.data.get("error", "")

    product_payload = {
        "name": "Invalid Date Product",
        "brand": "Test",
        "price_in_RS": 100,
        "quantity": 10,
        "manufacture_date": "2024-01-01",
        "expiry_date": "2023-01-01",
        "category": [category_id]
    }
    response = api_client.post("/products/", product_payload, format="json")
    assert response.status_code == 400
    assert "Expiry date cannot be before manufacture date" in response.data.get("error", "")

def test_get_all_products(api_client):
    response = api_client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_get_product_by_id(api_client):
    category_response = api_client.post("/products/categories/", {
        "category_name": "Stationery",
        "description": "Office items"
    }, format="json")
    category_id = category_response.data["id"]

    product_payload = {
        "name": "Notebook",
        "brand": "Classmate",
        "price_in_RS": 40,
        "quantity": 100,
        "manufacture_date": "2024-01-01",
        "expiry_date": "2025-01-01",
        "category": [category_id]
    }
    product_response = api_client.post("/products/", product_payload, format="json")
    product_id = product_response.data["id"]

    response = api_client.get(f"/products/{product_id}/")
    assert response.status_code == 200
    assert response.data["id"] == product_id

def test_update_product(api_client):
    category_response = api_client.post("/products/categories/", {
        "category_name": "Gadgets",
        "description": "Electronic gadgets"
    }, format="json")
    category_id = category_response.data["id"]

    product_payload = {
        "name": "Smartwatch",
        "brand": "Fossil",
        "price_in_RS": 7000,
        "quantity": 15,
        "manufacture_date": "2023-05-01",
        "expiry_date": "2025-05-01",
        "category": [category_id]
    }
    product_response = api_client.post("/products/", product_payload, format="json")
    product_id = product_response.data["id"]

    update_payload = {
        "price_in_RS": 6500,
        "quantity": 10
    }
    response = api_client.put(f"/products/{product_id}/", update_payload, format="json")
    assert response.status_code == 200
    assert response.data["price_in_RS"] == 6500
    assert response.data["quantity"] == 10

def test_delete_product(api_client):
    category_response = api_client.post("/products/categories/", {
        "category_name": "Clothing",
        "description": "Wearables"
    }, format="json")
    category_id = category_response.data["id"]

    product_payload = {
        "name": "T-Shirt",
        "brand": "H&M",
        "price_in_RS": 399,
        "quantity": 30,
        "manufacture_date": "2024-03-01",
        "expiry_date": "2026-03-01",
        "category": [category_id]
    }
    product_response = api_client.post("/products/", product_payload, format="json")
    product_id = product_response.data["id"]

    response = api_client.delete(f"/products/{product_id}/")
    assert response.status_code == 204

    get_response = api_client.get(f"/products/{product_id}/")
    assert get_response.status_code == 404
