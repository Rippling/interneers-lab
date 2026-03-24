import json

from bson import ObjectId
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, SimpleTestCase

from product_csr.models import Product, ProductCategory
from product_csr.seed import clear_product_csr_data, seed_product_csr_data


class ProductCsrIntegrationTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        clear_product_csr_data()
        self.seeded = seed_product_csr_data()

    def tearDown(self):
        clear_product_csr_data()

    def make_id(self):
        return str(ObjectId())

    # Categories

    def test_get_categories_returns_seeded_data(self):
        response = self.client.get("/product-csr/categories/")

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertIn("categories", body)
        self.assertEqual(len(body["categories"]), 3)

    def test_create_category_creates_new_record(self):
        payload = {
            "title": "Books",
            "description": "Books category",
        }

        response = self.client.post(
            "/product-csr/categories/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)

        self.assertEqual(body["title"], "Books")
        self.assertIsNotNone(ProductCategory.objects(title="Books").first())

    def test_create_category_fails_when_title_missing(self):
        payload = {
            "description": "Missing title",
        }

        response = self.client.post(
            "/product-csr/categories/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Title is required")

    def test_get_single_category_returns_expected_category(self):
        category = self.seeded["categories"]["electronics"]

        response = self.client.get(f"/product-csr/categories/{category.id}/")

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(body["title"], "Electronics")
        self.assertEqual(body["description"], "Devices and gadgets")

    def test_get_single_category_fails_when_not_found(self):
        response = self.client.get(f"/product-csr/categories/{self.make_id()}/")

        self.assertEqual(response.status_code, 404)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "category not found")

    def test_update_category_updates_record(self):
        category = self.seeded["categories"]["fashion"]

        payload = {
            "title": "Updated Fashion",
            "description": "Updated description",
        }

        response = self.client.put(
            f"/product-csr/categories/{category.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        category.reload()
        self.assertEqual(category.title, "Updated Fashion")
        self.assertEqual(category.description, "Updated description")

    def test_update_category_fails_when_not_found(self):
        payload = {
            "title": "Updated Fashion",
            "description": "Updated description",
        }

        response = self.client.put(
            f"/product-csr/categories/{self.make_id()}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "category not found")

    def test_delete_category_deletes_record(self):
        category = self.seeded["categories"]["home"]

        response = self.client.delete(f"/product-csr/categories/{category.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ProductCategory.objects(id=category.id).first())

    def test_delete_category_fails_when_not_found(self):
        response = self.client.delete(f"/product-csr/categories/{self.make_id()}/")

        self.assertEqual(response.status_code, 404)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "category not found")

    # Products

    def test_get_all_products_returns_seeded_products(self):
        response = self.client.get("/product-csr/products/")

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertIn("products", body)
        self.assertEqual(len(body["products"]), 3)

    def test_get_products_by_brand_filter_returns_matching_products(self):
        response = self.client.get("/product-csr/products/?brand=Apple")

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 1)
        self.assertEqual(body["products"][0]["name"], "iPhone 15")

    def test_get_products_by_search_filter_returns_matching_products(self):
        response = self.client.get("/product-csr/products/?search=Phone")

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 1)
        self.assertEqual(body["products"][0]["name"], "iPhone 15")

    def test_get_products_by_category_filter_returns_matching_products(self):
        category = self.seeded["categories"]["electronics"]

        response = self.client.get(f"/product-csr/products/?categories={category.id}")

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 2)

    def test_create_product_creates_new_record(self):
        payload = {
            "name": "MacBook Air",
            "brand": "Apple",
            "price": 1200.0,
            "quantity": 6,
        }

        response = self.client.post(
            "/product-csr/products/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        body = json.loads(response.content)

        self.assertEqual(body["name"], "MacBook Air")
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
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "name is required")

    def test_create_product_fails_when_brand_missing(self):
        payload = {
            "name": "MacBook Air",
            "price": 1200.0,
            "quantity": 6,
        }

        response = self.client.post(
            "/product-csr/products/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "brand is required")

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
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "price is required")

    def test_create_product_fails_when_quantity_missing(self):
        payload = {
            "name": "MacBook Air",
            "brand": "Apple",
            "price": 1200.0,
        }

        response = self.client.post(
            "/product-csr/products/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "quantity is required")

    def test_update_product_updates_record(self):
        product = self.seeded["products"]["iphone"]

        payload = {
            "name": "iPhone 15 Pro",
            "brand": "Apple",
            "price": 999.0,
            "quantity": 7,
        }

        response = self.client.put(
            f"/product-csr/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        product.reload()
        self.assertEqual(product.name, "iPhone 15 Pro")
        self.assertEqual(product.price, 999.0)
        self.assertEqual(product.quantity, 7)

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
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Product not found")

    def test_update_product_fails_when_brand_empty(self):
        product = self.seeded["products"]["iphone"]

        payload = {
            "brand": "",
        }

        response = self.client.put(
            f"/product-csr/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Brand cannot be empty")

    def test_update_product_fails_when_price_not_positive(self):
        product = self.seeded["products"]["iphone"]

        payload = {
            "price": 0,
        }

        response = self.client.put(
            f"/product-csr/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Price must be positive")

    def test_delete_product_deletes_record(self):
        product = self.seeded["products"]["galaxy"]

        response = self.client.delete(f"/product-csr/products/{product.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Product.objects(id=product.id).first())

    def test_delete_product_fails_when_not_found(self):
        response = self.client.delete(f"/product-csr/products/{self.make_id()}/")

        self.assertEqual(response.status_code, 404)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Product not found")

    # Category / product relationship

    def test_get_products_by_category_returns_products(self):
        category = self.seeded["categories"]["electronics"]

        response = self.client.get(f"/product-csr/categories/{category.id}/products/")

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(len(body["products"]), 2)

    def test_get_products_by_category_fails_when_category_not_found(self):
        response = self.client.get(f"/product-csr/categories/{self.make_id()}/products/")

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Category not found")

    def test_add_product_to_category_updates_product(self):
        category = self.seeded["categories"]["home"]
        product = self.seeded["products"]["tshirt"]

        response = self.client.post(
            f"/product-csr/categories/{category.id}/add-product/",
            data=json.dumps({"product_id": str(product.id)}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        product.reload()
        self.assertEqual(str(product.category.id), str(category.id))

    def test_add_product_to_category_fails_when_product_not_found(self):
        category = self.seeded["categories"]["home"]

        response = self.client.post(
            f"/product-csr/categories/{category.id}/add-product/",
            data=json.dumps({"product_id": self.make_id()}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Product not found")

    def test_add_product_to_category_fails_when_category_not_found(self):
        product = self.seeded["products"]["tshirt"]

        response = self.client.post(
            f"/product-csr/categories/{self.make_id()}/add-product/",
            data=json.dumps({"product_id": str(product.id)}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Category not found")

    def test_remove_product_from_category_updates_product(self):
        product = self.seeded["products"]["iphone"]

        response = self.client.post(
            "/product-csr/categories/dummy/remove-product/",
            data=json.dumps({"product_id": str(product.id)}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        product.reload()
        self.assertIsNone(product.category)

    def test_remove_product_from_category_fails_when_product_not_found(self):
        response = self.client.post(
            "/product-csr/categories/dummy/remove-product/",
            data=json.dumps({"product_id": self.make_id()}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Product not found")

    # Bulk upload

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
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(body["uploaded"], 2)
        self.assertEqual(body["skipped"], 0)
        self.assertIsNotNone(Product.objects(name="Pixel 8").first())
        self.assertIsNotNone(Product.objects(name="AirPods").first())

    def test_bulk_upload_fails_when_file_missing(self):
        response = self.client.post("/product-csr/products/bulk-upload/", data={})

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "CSV file is required")

    def test_bulk_upload_fails_when_csv_empty(self):
        upload = SimpleUploadedFile(
            "products.csv",
            b"",
            content_type="text/csv",
        )

        response = self.client.post(
            "/product-csr/products/bulk-upload/",
            data={"file": upload},
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Empty CSV file")

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
        )

        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Missing column: brand")

    def test_bulk_upload_skips_invalid_rows(self):
        csv_content = (
            "name,price,quantity,brand\n"
            "Pixel 8,699.0,5,Google\n"
            "Bad Price,abc,5,BrandX\n"
            "No Brand,100.0,2,\n"
        )

        upload = SimpleUploadedFile(
            "products.csv",
            csv_content.encode("utf-8"),
            content_type="text/csv",
        )

        response = self.client.post(
            "/product-csr/products/bulk-upload/",
            data={"file": upload},
        )

        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)

        self.assertEqual(body["uploaded"], 1)
        self.assertEqual(body["skipped"], 2)

    # Method not allowed

    def test_product_detail_get_is_method_not_allowed(self):
        product = self.seeded["products"]["iphone"]

        response = self.client.get(f"/product-csr/products/{product.id}/")

        self.assertEqual(response.status_code, 405)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Method not allowed")

    def test_category_products_post_is_method_not_allowed(self):
        category = self.seeded["categories"]["electronics"]

        response = self.client.post(f"/product-csr/categories/{category.id}/products/")

        self.assertEqual(response.status_code, 405)
        body = json.loads(response.content)
        self.assertEqual(body["error"], "Method not allowed")
