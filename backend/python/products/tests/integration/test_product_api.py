import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

def test_list_products(client, seeded_products):

    url = reverse("products")

    response = client.get(url)

    assert response.status_code == 200

    assert "products" in response.data
    assert len(response.data["products"]) == 2

def test_list_products_sorted(client, seeded_products):

    url = reverse("products")

    response = client.get(url, {"sort_by": "price"})

    assert response.status_code == 200

    products = response.data["products"]

    assert products[0]["price"] <= products[1]["price"]

def test_create_product(client, seeded_categories):

    category_id = str(seeded_categories[0])

    data = {
        "name": "Banana",
        "price": 5,
        "category": category_id,
        "brand": "Fruit Brand",
        "quantity": 30
    }

    url = reverse("products")

    response = client.post(url, data, format="json")

    assert response.status_code == 201

    product = response.data["product created"]

    assert product["name"] == "Banana"
    assert product["price"] == 5

def test_create_product_invalid_data(client):

    data = {
        "name": "",
        "price": -10
    }

    url = reverse("products")

    response = client.post(url, data, format="json")

    assert response.status_code == 400

def test_get_product(client, seeded_products):

    product_id = str(seeded_products[0])

    url = reverse("product_detail", args=[product_id])

    response = client.get(url)

    assert response.status_code == 200

    product = response.data["product"]

    assert product["name"] == "Apple"

def test_update_product(client, seeded_products, seeded_categories):

    product_id = str(seeded_products[0])
    category_id = str(seeded_categories[0])

    data = {
        "name": "Green Apple",
        "price": 12,
        "category": category_id,
        "brand": "Fruit Brand",
        "quantity": 60
    }

    url = reverse("product_detail", args=[product_id])

    response = client.put(url, data, format="json")

    assert response.status_code == 200

    updated_product = response.data["product updated"]

    assert updated_product["name"] == "Green Apple"
    assert updated_product["price"] == 12

def test_patch_product(client, seeded_products):

    product_id = str(seeded_products[0])

    data = {
        "price": 20
    }

    url = reverse("product_detail", args=[product_id])

    response = client.patch(url, data, format="json")

    assert response.status_code == 200

    updated_product = response.data["product updated"]

    assert updated_product["price"] == 20

def test_delete_product(client, seeded_products):

    product_id = str(seeded_products[0])

    url = reverse("product_detail", args=[product_id])

    response = client.delete(url)

    assert response.status_code == 200

def test_get_product_invalid_id(client):

    url = reverse("product_detail", args=["invalid-id"])

    response = client.get(url)

    assert response.status_code == 400 or response.status_code == 404        