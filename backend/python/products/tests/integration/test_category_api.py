import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()

def test_list_categories(client, seeded_categories):

    url=reverse("categories")
    response = client.get(url)

    assert response.status_code == 200
    print(response)
    assert len(response.data["categories"]) == 2

def test_create_category(client, seeded_categories):

    data = {
        "name": "Dairy",
        "description": "Milk products"
    }
    url=reverse("categories")
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert response.data["category created"]["name"] == "Dairy"

def test_get_category_detail(client, seeded_categories):

    category_id = str(seeded_categories[0])

    response = client.get(f"/categories/{category_id}/")

    assert response.status_code == 200
    assert response.data["category"]["name"] == "Fruits"

def test_update_category(client, seeded_categories):

    category_id = str(seeded_categories[0])

    data = {
        "name": "Fresh Fruits",
        "description": "Updated description"
    }

    response = client.put(
        f"/categories/{category_id}/",
        data,
        format="json"
    )

    assert response.status_code == 200
    assert response.data["category updated"]["name"] == "Fresh Fruits"

def test_patch_category(client, seeded_categories):

    category_id = str(seeded_categories[0])

    data = {"name": "Patched Fruits"}

    response = client.patch(
        f"/categories/{category_id}/",
        data,
        format="json"
    )

    assert response.status_code == 200

def test_products_by_category(client, seeded_categories, seeded_products):

    category_id = str(seeded_categories[0])
    print(category_id)
    response = client.get(f"/categories/{category_id}/products/")
    print(response)
    assert response.status_code == 200
    assert len(response.data["products"]) >= 1

def test_delete_category(client, seeded_categories):

    category_id = str(seeded_categories[0])
    
    url=reverse("category_detail", args=[category_id])
    response = client.delete(url)

    assert response.status_code == 200    

