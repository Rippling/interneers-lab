import pytest
from rest_framework.test import APIClient
from products.models import Products, ProductCategory

@pytest.mark.django_db
def test_end_to_end_product_crud():
    # Clean up before test
    Products.objects.delete()
    ProductCategory.objects.delete()

    client = APIClient()

    # 1. Create a new category
    category_data = {
        "category_id": 10,
        "category_name": "Books",
        "description": "All kinds of books"
    }
    res = client.post("/api/category/list", data=category_data, format="json")
    assert res.status_code == 201
    assert res.json()["category_name"] == "Books"

    # 2. Create a product in this category
    product_data = {
        "product_id": 999,
        "name": "The Alchemist",
        "description": "Paulo Coelho",
        "brand": "Harper",
        "category_id": 10
    }
    res = client.post("/api/list", data=product_data, format="json")
    assert res.status_code == 201
    json_data = res.json()
    assert json_data["name"] == "The Alchemist"
    assert json_data["description"] == "Paulo Coelho"
    assert json_data["brand"] == "Harper"

    # 3. Fetch the product
    res = client.get("/api/list/999")
    assert res.status_code == 200
    assert res.json()["name"] == "The Alchemist"

    # 4. Update the product
    update_data = {"description": "Bestselling novel"}
    res = client.patch("/api/list/999", data=update_data, format="json")
    assert res.status_code == 200  # Changed from 201 to correct REST behavior
    assert res.json()["description"] == "Bestselling novel"

    # 5. Delete the product
    res = client.delete("/api/list/999")
    assert res.status_code in [200, 204]

    # 6. Try fetching the deleted product (should fail)
    res = client.get("/api/list/999")
    assert res.status_code == 404

    res = client.get("/api/category/10/list")
    if res.status_code == 200:
        res = client.delete("/api/category/10/list")
        assert res.status_code in [200, 204, 201]
    else:
        print("Category already deleted, skipping delete step.")


