import pytest
from django.urls import reverse
from rest_framework import status
from django_app.models.product import Product
from django_app.models.category import Category
from django_app.services.product_service import ProductService
from bson import ObjectId


@pytest.mark.django_db
class TestProductIntegration:

    def test_create_product(self, api_client, seeded_data):
        category = Category.objects.get(title="Electronics")
        url = reverse("product-list")
        payload = {
            "name": "Smartphone",
            "description": "Latest model with high-end features",
            "brand": "BrandX",
            "price": 599.99,
            "quantity": 100,
            "category": str(category.title)
        }
        res = api_client.post(url, payload, format="json")
        print("debugging:",res.data)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["created_product"]["name"] == "Smartphone"

    def test_list_products(self, api_client, seeded_data):
        url = reverse("product-list")
        res = api_client.get(url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data["results"]) == Product.objects.count()

    def test_get_single_product(self, api_client, seeded_data):
        product = Product.objects.first()
        url = reverse("product-detail", kwargs={"pk": str(product.id)})
        res = api_client.get(url)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["name"] == product.name

    def test_update_product(self, api_client, seeded_data):
        product = Product.objects.first()
        url = reverse("product-detail", kwargs={"pk": str(product.id)})
        payload = {
            "name": "Updated Smartphone",
            "description": "Updated features and specs",
            "brand": "BrandX",
            "price": 649.99,
            "quantity": 50,
            "category": str(product.category.title)
        }
        res = api_client.put(url, payload, format="json")
        assert res.status_code == status.HTTP_200_OK
        assert res.data["updated_product"]["name"] == "Updated Smartphone"

    def test_delete_product(self, api_client, seeded_data):
        product = Product.objects.first()
        url = reverse("product-detail", kwargs={"pk": str(product.id)})
        res = api_client.delete(url)
        assert res.status_code == status.HTTP_200_OK
        assert f"Product '{product.name}' deleted successfully" in res.data["message"]

    def test_invalid_product_id(self, api_client):
        invalid_id = "5f4e7b1a2c3d4e5f6a7b8c9d"  # Non-existing or invalid ID
        url = reverse("product-detail", kwargs={"pk": invalid_id})
        res = api_client.get(url)
        assert res.status_code == status.HTTP_404_NOT_FOUND
        assert "No product found with ID" in res.data.get("message", "")

    def test_create_product_invalid_data(self, api_client):
        category = Category.objects.get(title="Electronics")
        url = reverse("product-list")
        payload = {
            "name": "",  # Invalid name
            "description": "A new product without name",
            "brand": "BrandX",
            "price": -10,  # Invalid price
            "quantity": 50,
            "category": str(category.id)
        }
        res = api_client.post(url, payload, format="json")
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "Validation error" in res.data["error"]

    def test_list_products_with_filters(self, api_client, seeded_data):
        category = Category.objects.get(title="Electronics")
        url = reverse("product-list")
        res = api_client.get(url, {"categories": [str(category.id)], "price_min": 100, "price_max": 1000})
        assert res.status_code == status.HTTP_200_OK
        assert all(product["price"] >= 100 and product["price"] <= 1000 for product in res.data["results"])

    def test_invalid_page_size(self, api_client):
        url = reverse("product-list")
        res = api_client.get(url, {"page_size": "invalid"})
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid page size" in res.data["error"]

    def test_retrieve_product_invalid_id(self, api_client):
        invalid_id = "invalid_id"
        url = reverse("product-detail", kwargs={"pk": invalid_id})
        res = api_client.get(url)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid product ID" in res.data["error"]
