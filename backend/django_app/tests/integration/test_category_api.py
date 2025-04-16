import pytest
from django.urls import reverse
from django_app.models.category import Category
from django_app.models.product import Product

@pytest.mark.django_db
class TestCategoryIntegration:

    def test_create_category(self, api_client):
        url = reverse("category-list")
        payload = {
            "title": "Fitness",
            "description": "Gym and workout equipment"
        }
        res = api_client.post(url, payload, format="json")
        assert res.status_code == 200
        assert res.data["created_category"]["title"] == "Fitness"

    def test_list_categories(self, api_client, seeded_data):
        url = reverse("category-list")
        res = api_client.get(url)
        assert res.status_code == 200
        assert len(res.data["results"]) == Category.objects.count()

    def test_get_single_category(self, api_client, seeded_data):
        category = Category.objects.get(title="Electronics")
        url = reverse("category-detail", kwargs={"pk": str(category.id)})
        res = api_client.get(url)
        assert res.status_code == 200
        assert res.data["title"] == "Electronics"

    def test_update_category(self, api_client, seeded_data):
        category = Category.objects.get(title="Books")
        url = reverse("category-detail", kwargs={"pk": str(category.id)})
        payload = {
            "title": "Novels",
            "description": "Fictional and non-fictional books"
        }
        res = api_client.put(url, payload, format="json")
        assert res.status_code == 200
        assert res.data["updated_category"]["title"] == "Novels"

    def test_delete_category(self, api_client, seeded_data):
        category = Category.objects.get(title="Clothing")
        url = reverse("category-detail", kwargs={"pk": str(category.id)})
        res = api_client.delete(url)
        assert res.status_code == 200
        assert f"{category.title}" in res.data["message"]

    def test_list_category_products(self, api_client, seeded_data):
        category = Category.objects.get(title="Home Appliances")
        url = reverse("category-products", kwargs={"pk": str(category.id)})
        res = api_client.get(url)
        assert res.status_code == 200
        assert "category" in res.data
        assert isinstance(res.data["results"], list)

    def test_add_product_to_category(self, api_client, seeded_data):
        category = Category.objects.get(title="Electronics")
        url = reverse("category-add-product", kwargs={"pk": str(category.id)})
        payload = {
            "name": "Wireless Mouse",
            "description": "A high-quality wireless mouse",
            "brand": "Logitech",
            "price": 49.99,
            "quantity": 25
        }
        res = api_client.post(url, payload, format="json")
        print(res.data)
        assert res.status_code in [200, 201]

    def test_remove_product_from_category(self, api_client, seeded_data):
        category = Category.objects.get(title="Books")
        product = Product.objects.filter(category=category).first()
        assert product is not None
        url = reverse(
            "category-remove-product",
            kwargs={"pk": str(category.id), "product_id": str(product.id)}
        )
        res = api_client.delete(url)
        assert res.status_code in [200, 204]

    def test_remove_product_from_empty_category(self, api_client, seeded_data):
        category = Category.objects.get(title="Books")
        products_in_category = Product.objects.filter(category=category)
        products_in_category.delete()
        products_in_category = Product.objects.filter(category=category)
        assert not products_in_category

        invalid_product_id = "5f4e7b1a2c3d4e5f6a7b8c9d"

        url = reverse(
            "category-remove-product",
            kwargs={"pk": str(category.id), "product_id": invalid_product_id}
        )
        res = api_client.delete(url)
        assert res.status_code == 404
        assert "No product found with ID" in res.data.get("message", "")
        assert category.title in res.data.get("message", "") 





