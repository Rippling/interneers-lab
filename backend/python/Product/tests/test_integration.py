"""
Integration tests for the Product API.

These tests hit the actual Django views end-to-end:
  HTTP request → URL routing → View → Service → Repository → MongoDB → Response

Unlike unit tests (which mock the repository), integration tests use a real
MongoDB connection — pointed at the test database defined in settings.py
(MONGO_TEST_DB, defaults to interneers_lab_test).

Every test class cleans up all documents it creates in tearDown so tests
are fully isolated from each other and from real data.

Run with:
    python manage.py test Product.tests.test_integration
"""

import json
from django.test import SimpleTestCase, Client
from Product.models import Product, ProductCategory
from io import BytesIO

# ---------------------------------------------------------------------------
# Base class — shared setup and helpers used by all test classes
# ---------------------------------------------------------------------------

class BaseAPITest(SimpleTestCase):
    """
    Base class for all API integration tests.

    Provides:
      - A Django test Client pre-configured with JSON headers
      - Helper methods for common API calls
      - tearDown that wipes all Product and ProductCategory documents
        so each test starts with a clean database
    """

    def setUp(self):
        self.client = Client()
        # Clean before each test too — ensures a fresh state
        # regardless of what previous tests left behind
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()

    def tearDown(self):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()

    # --- helpers ---

    def create_category(self, title="Electronics", description="Test category"):
        response = self.client.post(
            "/categories/",
            data=json.dumps({"title": title, "description": description}),
            content_type="application/json",
        )
        return response

    def create_product(self, name="iPhone 15", price=999.99, brand="Apple",
                       quantity=50, description="A smartphone",
                       category_id=None):
        data = {
            "name": name,
            "description": description,
            "price": price,
            "brand": brand,
            "quantity": quantity,
        }
        if category_id:
            data["category_id"] = category_id
        response = self.client.post(
            "/products/",
            data=json.dumps(data),
            content_type="application/json",
        )
        return response


# ---------------------------------------------------------------------------
# Category CRUD
# ---------------------------------------------------------------------------

class TestCategoryAPI(BaseAPITest):

    def test_create_category_returns_201(self):
        response = self.create_category()
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)
        self.assertIn("category", body)
        self.assertEqual(body["category"]["title"], "Electronics")

    def test_create_category_missing_title_returns_400(self):
        response = self.client.post(
            "/categories/",
            data=json.dumps({"description": "No title"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertIn("title", body["details"])

    def test_get_category_returns_200(self):
        created = json.loads(self.create_category().content)
        cat_id = created["category"]["id"]
        response = self.client.get(f"/categories/{cat_id}/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["title"], "Electronics")

    def test_get_category_not_found_returns_404(self):
        response = self.client.get("/categories/000000000000000000000000/")
        self.assertEqual(response.status_code, 404)

    def test_list_categories_returns_200(self):
        self.create_category("Electronics", "desc")
        self.create_category("Food", "desc")
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_categories"], 2)

    def test_patch_category_updates_field(self):
        created = json.loads(self.create_category().content)
        cat_id = created["category"]["id"]
        response = self.client.patch(
            f"/categories/{cat_id}/",
            data=json.dumps({"description": "Updated desc"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["category"]["description"], "Updated desc")
        self.assertEqual(body["category"]["title"], "Electronics")

    def test_put_category_requires_all_fields(self):
        created = json.loads(self.create_category().content)
        cat_id = created["category"]["id"]
        response = self.client.put(
            f"/categories/{cat_id}/",
            data=json.dumps({"title": "Only title"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_category_returns_204(self):
        created = json.loads(self.create_category().content)
        cat_id = created["category"]["id"]
        response = self.client.delete(f"/categories/{cat_id}/")
        self.assertEqual(response.status_code, 204)
        # Verify it's gone
        get_response = self.client.get(f"/categories/{cat_id}/")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_category_blocked_when_products_exist(self):
        cat = json.loads(self.create_category().content)
        cat_id = cat["category"]["id"]
        self.create_product(category_id=cat_id)
        response = self.client.delete(f"/categories/{cat_id}/")
        self.assertEqual(response.status_code, 409)
        body = json.loads(response.content)
        self.assertIn("product(s)", body["error"])

    def test_get_products_in_category(self):
        cat = json.loads(self.create_category().content)
        cat_id = cat["category"]["id"]
        self.create_product(name="iPhone", category_id=cat_id)
        self.create_product(name="iPad", category_id=cat_id)
        self.create_product(name="Cable")  # no category
        response = self.client.get(f"/categories/{cat_id}/products/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 2)


# ---------------------------------------------------------------------------
# Product CRUD
# ---------------------------------------------------------------------------

class TestProductAPI(BaseAPITest):

    def test_create_product_returns_201(self):
        response = self.create_product()
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)
        self.assertIn("product", body)
        self.assertEqual(body["product"]["name"], "iPhone 15")

    def test_create_product_with_category(self):
        cat = json.loads(self.create_category().content)
        cat_id = cat["category"]["id"]
        response = self.create_product(category_id=cat_id)
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)
        self.assertEqual(body["product"]["category"]["title"], "Electronics")

    def test_create_product_without_category(self):
        response = self.create_product()
        body = json.loads(response.content)
        self.assertIsNone(body["product"]["category"])

    def test_create_product_invalid_category_id_returns_400(self):
        response = self.create_product(category_id="000000000000000000000000")
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertIn("not found", body["error"])

    def test_create_product_missing_fields_returns_400(self):
        response = self.client.post(
            "/products/",
            data=json.dumps({"name": "Incomplete"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertIn("details", body)

    def test_create_product_negative_price_returns_400(self):
        response = self.create_product(price=-10)
        self.assertEqual(response.status_code, 400)

    def test_create_product_boolean_price_rejected(self):
        response = self.create_product(price=True)
        self.assertEqual(response.status_code, 400)

    def test_get_product_returns_200(self):
        created = json.loads(self.create_product().content)
        prod_id = created["product"]["id"]
        response = self.client.get(f"/products/{prod_id}/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["name"], "iPhone 15")

    def test_get_product_not_found_returns_404(self):
        response = self.client.get("/products/000000000000000000000000/")
        self.assertEqual(response.status_code, 404)

    def test_list_products_returns_200(self):
        self.create_product(name="iPhone")
        self.create_product(name="iPad")
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 2)

    def test_list_products_pagination(self):
        for i in range(5):
            self.create_product(name=f"Product {i}")
        response = self.client.get("/products/?page=1&page_size=2")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body["products"]), 2)
        self.assertEqual(body["total_products"], 5)
        self.assertEqual(body["total_pages"], 3)

    def test_put_product_updates_all_fields(self):
        created = json.loads(self.create_product().content)
        prod_id = created["product"]["id"]
        response = self.client.put(
            f"/products/{prod_id}/",
            data=json.dumps({
                "name": "iPhone 16",
                "description": "Newer model",
                "price": 1099.99,
                "brand": "Apple",
                "quantity": 30,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["product"]["name"], "iPhone 16")
        self.assertEqual(body["product"]["price"], 1099.99)

    def test_patch_product_updates_price_only(self):
        created = json.loads(self.create_product().content)
        prod_id = created["product"]["id"]
        response = self.client.patch(
            f"/products/{prod_id}/",
            data=json.dumps({"price": 799.99}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["product"]["price"], 799.99)
        self.assertEqual(body["product"]["name"], "iPhone 15")

    def test_patch_product_category_unchanged_when_not_sent(self):
        cat = json.loads(self.create_category().content)
        cat_id = cat["category"]["id"]
        created = json.loads(self.create_product(category_id=cat_id).content)
        prod_id = created["product"]["id"]
        # Patch only price — category_id not in body
        self.client.patch(
            f"/products/{prod_id}/",
            data=json.dumps({"price": 500.0}),
            content_type="application/json",
        )
        # Fetch and verify category still set
        response = self.client.get(f"/products/{prod_id}/")
        body = json.loads(response.content)
        self.assertEqual(body["category"]["title"], "Electronics")

    def test_delete_product_returns_204(self):
        created = json.loads(self.create_product().content)
        prod_id = created["product"]["id"]
        response = self.client.delete(f"/products/{prod_id}/")
        self.assertEqual(response.status_code, 204)
        # Verify gone
        get_response = self.client.get(f"/products/{prod_id}/")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_product_not_found_returns_404(self):
        response = self.client.delete("/products/000000000000000000000000/")
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# Category membership endpoints
# ---------------------------------------------------------------------------

class TestProductCategoryMembership(BaseAPITest):

    def test_assign_product_to_category(self):
        cat = json.loads(self.create_category().content)
        cat_id = cat["category"]["id"]
        prod = json.loads(self.create_product().content)
        prod_id = prod["product"]["id"]

        response = self.client.put(
            f"/products/{prod_id}/category/",
            data=json.dumps({"category_id": cat_id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["product"]["category"]["title"], "Electronics")

    def test_assign_product_missing_category_id_returns_400(self):
        prod = json.loads(self.create_product().content)
        prod_id = prod["product"]["id"]
        response = self.client.put(
            f"/products/{prod_id}/category/",
            data=json.dumps({}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_remove_product_from_category(self):
        cat = json.loads(self.create_category().content)
        cat_id = cat["category"]["id"]
        prod = json.loads(self.create_product(category_id=cat_id).content)
        prod_id = prod["product"]["id"]

        response = self.client.delete(f"/products/{prod_id}/category/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertIsNone(body["product"]["category"])

    def test_remove_product_not_in_category_returns_400(self):
        prod = json.loads(self.create_product().content)
        prod_id = prod["product"]["id"]
        response = self.client.delete(f"/products/{prod_id}/category/")
        self.assertEqual(response.status_code, 400)


# ---------------------------------------------------------------------------
# Rich filters on GET /products/
# ---------------------------------------------------------------------------

class TestProductFilters(BaseAPITest):

    def setUp(self):
        super().setUp()
        # Create two categories
        self.electronics = json.loads(self.create_category("Electronics", "desc").content)["category"]
        self.food = json.loads(self.create_category("Food", "desc").content)["category"]

        # Create products across categories and price ranges
        self.create_product(name="iPhone", price=999.99, brand="Apple",
                            quantity=50, category_id=self.electronics["id"])
        self.create_product(name="MacBook", price=1999.99, brand="Apple",
                            quantity=10, category_id=self.electronics["id"])
        self.create_product(name="Bread", price=2.99, brand="Bakery",
                            quantity=200, category_id=self.food["id"])
        self.create_product(name="Cable", price=9.99, brand="Anker",
                            quantity=100)  # no category

    def test_filter_by_single_category(self):
        response = self.client.get(f"/products/?category_ids={self.electronics['id']}")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 2)
        names = [p["name"] for p in body["products"]]
        self.assertIn("iPhone", names)
        self.assertIn("MacBook", names)

    def test_filter_by_multiple_categories(self):
        response = self.client.get(
            f"/products/?category_ids={self.electronics['id']},{self.food['id']}"
        )
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 3)

    def test_filter_by_min_price(self):
        response = self.client.get("/products/?min_price=100")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        for product in body["products"]:
            self.assertGreaterEqual(product["price"], 100)

    def test_filter_by_price_range(self):
        response = self.client.get("/products/?min_price=5&max_price=1000")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        for product in body["products"]:
            self.assertGreaterEqual(product["price"], 5)
            self.assertLessEqual(product["price"], 1000)

    def test_filter_min_price_greater_than_max_price_returns_400(self):
        response = self.client.get("/products/?min_price=500&max_price=100")
        self.assertEqual(response.status_code, 400)

    def test_filter_by_brand(self):
        response = self.client.get("/products/?brand=Apple")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 2)
        for product in body["products"]:
            self.assertEqual(product["brand"], "Apple")

    def test_filter_by_search(self):
        response = self.client.get("/products/?search=mac")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 1)
        self.assertEqual(body["products"][0]["name"], "MacBook")

    def test_filter_by_min_quantity(self):
        response = self.client.get("/products/?min_quantity=100")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        for product in body["products"]:
            self.assertGreaterEqual(product["quantity"], 100)

    def test_combined_filters(self):
        response = self.client.get(
            f"/products/?brand=Apple&min_price=500&category_ids={self.electronics['id']}"
        )
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 2)

    def test_filter_invalid_category_id_returns_400(self):
        response = self.client.get("/products/?category_ids=000000000000000000000000")
        self.assertEqual(response.status_code, 400)

    def test_no_filters_returns_all(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(body["total_products"], 4)


# ---------------------------------------------------------------------------
# Bulk CSV import
# ---------------------------------------------------------------------------

class TestBulkCSVImport(BaseAPITest):

    def test_bulk_create_valid_csv(self):
        csv_content = (
            "name,description,price,brand,quantity\n"
            "MacBook Pro,Apple laptop,1999.99,Apple,30\n"
            "iPad Air,Apple tablet,799.99,Apple,75\n"
        )
        csv_file = csv_content.encode("utf-8")
        response = self.client.post(
            "/products/bulk/",
            data={"file": BytesIO(csv_content.encode("utf-8"))},
        )
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)
        self.assertEqual(body["total_created"], 2)

    def test_bulk_create_with_category(self):
        cat = json.loads(self.create_category().content)
        cat_id = cat["category"]["id"]
        csv_content = (
            f"name,description,price,brand,quantity,category_id\n"
            f"MacBook Pro,Apple laptop,1999.99,Apple,30,{cat_id}\n"
        )
        csv_file = csv_content.encode("utf-8")
        
        response = self.client.post(
            "/products/bulk/",
            data={"file": BytesIO(csv_content.encode("utf-8"))},
        )
        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)
        self.assertEqual(body["products"][0]["category"]["title"], "Electronics")

    def test_bulk_create_invalid_row_rejects_all(self):
        csv_content = (
            "name,description,price,brand,quantity\n"
            "Valid Product,Good,99.99,Brand,10\n"
            "Bad Product,,not-a-price,,-5\n"
        )
        csv_file = csv_content.encode("utf-8")
        response = self.client.post(
            "/products/bulk/",
            data={"file": BytesIO(csv_content.encode("utf-8"))},
        )
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertIn("failed_rows", body)
        # Nothing inserted
        self.assertEqual(Product.objects.count(), 0)

    def test_bulk_create_missing_column_returns_400(self):
        csv_content = (
            "name,price,brand,quantity\n"  # missing description
            "MacBook Pro,1999.99,Apple,30\n"
        )
        csv_file = csv_content.encode("utf-8")
        response = self.client.post(
            "/products/bulk/",
            data={"file": BytesIO(csv_content.encode("utf-8"))},
        )
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertIn("missing_columns", body)

    def test_bulk_create_no_file_returns_400(self):
        response = self.client.post("/products/bulk/")
        self.assertEqual(response.status_code, 400)