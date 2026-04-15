import json

from bson import ObjectId
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from rest_framework.authtoken.models import Token

from product_csr.models import Product, ProductCategory
from product_csr.seed import clear_product_csr_data


class ProductCsrIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        clear_product_csr_data()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
        )
        self.token = Token.objects.create(user=self.user)
        self.auth_header = {
            "HTTP_AUTHORIZATION": f"Token {self.token.key}",
        }
        self.owner_id = str(self.user.id)

        self.electronics = ProductCategory(
            title="Electronics",
            description="Devices and gadgets",
            owner_id=self.owner_id,
        ).save()

        self.fashion = ProductCategory(
            title="Fashion",
            description="Clothing and accessories",
            owner_id=self.owner_id,
        ).save()

        self.home = ProductCategory(
            title="Home",
            description="Home essentials",
            owner_id=self.owner_id,
        ).save()

        self.iphone = Product(
            name="iPhone 15",
            brand="Apple",
            price=799.0,
            quantity=10,
            category=self.electronics,
            owner_id=self.owner_id,
        ).save()

        self.galaxy = Product(
            name="Galaxy S24",
            brand="Samsung",
            price=699.0,
            quantity=8,
            category=self.electronics,
            owner_id=self.owner_id,
        ).save()

        self.tshirt = Product(
            name="T-Shirt",
            brand="H&M",
            price=19.99,
            quantity=25,
            category=self.fashion,
            owner_id=self.owner_id,
        ).save()

    def tearDown(self):
        clear_product_csr_data()

    def make_id(self):
        return str(ObjectId())

    def test_get_categories_requires_authentication(self):
        response = self.client.get("/product-csr/categories/")

        self.assertEqual(response.status_code, 401)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Authentication required")

    def test_get_categories_returns_user_categories(self):
        response = self.client.get(
            "/product-csr/categories/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertIn("categories", body)
        self.assertEqual(len(body["categories"]), 3)
        self.assertEqual(body["categories"][0]["owner_id"], self.owner_id)

    def test_create_category_creates_new_record(self):
        payload = {
            "title": "Books",
            "description": "Books category",
        }

        response = self.client.post(
            "/product-csr/categories/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)

        self.assertEqual(body["title"], "Books")
        self.assertEqual(body["owner_id"], self.owner_id)
        self.assertIsNotNone(ProductCategory.objects(title="Books").first())

    def test_create_category_fails_when_title_missing(self):
        payload = {
            "description": "Missing title",
        }

        response = self.client.post(
            "/product-csr/categories/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Title is required")

    def test_get_single_category_returns_expected_category(self):
        response = self.client.get(
            f"/product-csr/categories/{self.electronics.id}/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(body["title"], "Electronics")
        self.assertEqual(body["description"], "Devices and gadgets")
        self.assertEqual(body["owner_id"], self.owner_id)

    def test_get_single_category_fails_when_not_found(self):
        response = self.client.get(
            f"/product-csr/categories/{self.make_id()}/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 404)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "category not found")

    def test_update_category_updates_record(self):
        payload = {
            "title": "Updated Fashion",
            "description": "Updated description",
        }

        response = self.client.put(
            f"/product-csr/categories/{self.fashion.id}/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)

        self.fashion.reload()
        self.assertEqual(self.fashion.title, "Updated Fashion")
        self.assertEqual(self.fashion.description, "Updated description")

    def test_delete_category_deletes_record(self):
        response = self.client.delete(
            f"/product-csr/categories/{self.home.id}/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ProductCategory.objects(id=self.home.id).first())

    def test_get_products_requires_authentication(self):
        response = self.client.get("/product-csr/products/")

        self.assertEqual(response.status_code, 401)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Authentication required")

    def test_get_all_products_returns_user_products(self):
        response = self.client.get(
            "/product-csr/products/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertIn("products", body)
        self.assertEqual(len(body["products"]), 3)
        self.assertEqual(body["products"][0]["owner_id"], self.owner_id)

    def test_get_products_by_brand_filter_returns_matching_products(self):
        response = self.client.get(
            "/product-csr/products/?brand=Apple",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 1)
        self.assertEqual(body["products"][0]["name"], "iPhone 15")

    def test_get_products_by_search_filter_returns_matching_products(self):
        response = self.client.get(
            "/product-csr/products/?search=Phone",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 1)
        self.assertEqual(body["products"][0]["name"], "iPhone 15")

    def test_get_products_by_category_filter_returns_matching_products(self):
        response = self.client.get(
            f"/product-csr/products/?categories={self.electronics.id}",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 2)

    def test_create_product_creates_new_record(self):
        payload = {
            "name": "MacBook Air",
            "brand": "Apple",
            "price": 1200.0,
            "quantity": 6,
            "categoryId": str(self.electronics.id),
        }

        response = self.client.post(
            "/product-csr/products/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)

        self.assertEqual(body["name"], "MacBook Air")
        self.assertEqual(body["owner_id"], self.owner_id)
        self.assertEqual(body["category"], str(self.electronics.id))
        self.assertIsNotNone(Product.objects(name="MacBook Air").first())

    def test_create_product_fails_when_name_missing(self):
        payload = {
            "brand": "Apple",
            "price": 1200.0,
            "quantity": 6,
        }

        response = self.client.post(
            "/product-csr/products/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "name is required")

    def test_create_product_fails_when_price_zero(self):
        payload = {
            "name": "MacBook Air",
            "brand": "Apple",
            "price": 0,
            "quantity": 6,
        }

        response = self.client.post(
            "/product-csr/products/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Price must be positive")

    def test_update_product_updates_record(self):
        payload = {
            "name": "iPhone 15 Pro",
            "brand": "Apple",
            "price": 999.0,
            "quantity": 7,
        }

        response = self.client.put(
            f"/product-csr/products/{self.iphone.id}/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)

        self.iphone.reload()
        self.assertEqual(self.iphone.name, "iPhone 15 Pro")
        self.assertEqual(self.iphone.price, 999.0)
        self.assertEqual(self.iphone.quantity, 7)

    def test_update_product_fails_when_not_found(self):
        payload = {
            "name": "Updated",
            "brand": "Apple",
            "price": 999.0,
            "quantity": 7,
        }

        response = self.client.put(
            f"/product-csr/products/{self.make_id()}/",
            data=json.dumps(payload),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Product not found")

    def test_delete_product_deletes_record(self):
        response = self.client.delete(
            f"/product-csr/products/{self.galaxy.id}/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Product.objects(id=self.galaxy.id).first())

    def test_delete_product_fails_when_not_found(self):
        response = self.client.delete(
            f"/product-csr/products/{self.make_id()}/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 404)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Product not found")

    def test_get_products_by_category_returns_products(self):
        response = self.client.get(
            f"/product-csr/categories/{self.electronics.id}/products/",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 2)

    def test_add_product_to_category_updates_product(self):
        response = self.client.post(
            f"/product-csr/categories/{self.home.id}/add-product/",
            data=json.dumps({"product_id": str(self.tshirt.id)}),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)

        self.tshirt.reload()
        self.assertEqual(str(self.tshirt.category.id), str(self.home.id))

    def test_remove_product_from_category_updates_product(self):
        response = self.client.post(
            "/product-csr/categories/dummy/remove-product/",
            data=json.dumps({"product_id": str(self.iphone.id)}),
            content_type="application/json",
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)

        self.iphone.reload()
        self.assertIsNone(self.iphone.category)

    def test_bulk_upload_products_creates_multiple_records(self):
        csv_content = (
            "name,price,quantity,brand\n"
            "Pixel 8,699.0,5,Google\n"
            "AirPods,199.0,12,Apple\n"
        )

        upload = SimpleUploadedFile(
            "products.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )

        response = self.client.post(
            "/product-csr/products/bulk-upload/",
            data={"file": upload},
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(body["uploaded"], 2)
        self.assertEqual(body["skipped"], 0)
        self.assertIsNotNone(Product.objects(name="Pixel 8").first())
        self.assertIsNotNone(Product.objects(name="AirPods").first())

    def test_bulk_upload_fails_when_file_missing(self):
        response = self.client.post(
            "/product-csr/products/bulk-upload/",
            data={},
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "CSV file is required")

    def test_bulk_upload_fails_when_required_column_missing(self):
        csv_content = (
            "name,price,quantity\n"
            "Pixel 8,699.0,5\n"
        )

        upload = SimpleUploadedFile(
            "products.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )

        response = self.client.post(
            "/product-csr/products/bulk-upload/",
            data={"file": upload},
            **self.auth_header,
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Missing column: brand")

    def test_product_detail_get_is_method_not_allowed(self):
        response = self.client.get(f"/product-csr/products/{self.iphone.id}/")

        self.assertEqual(response.status_code, 405)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Method not allowed")

    def test_category_products_post_is_method_not_allowed(self):
        response = self.client.post(
            f"/product-csr/categories/{self.electronics.id}/products/",
        )

        self.assertEqual(response.status_code, 405)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Method not allowed")
