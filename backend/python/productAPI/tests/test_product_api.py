from productAPI.models import Product
from productAPI.tests.integration_test_base import IntegrationTestBase


class TestProductListAPI(IntegrationTestBase):

    def test_get_all_products_returns_200(self):
        response = self.client.get("/api/product/")

        self.assertEqual(response.status_code, 200)

    def test_get_all_products_returns_correct_count(self):
        response = self.client.get("/api/product/")

        self.assertEqual(len(response.data), 4)

    def test_get_products_filter_by_category(self):
        response = self.client.get("/api/product/?categories=Food")

        self.assertEqual(len(response.data), 2)

    def test_get_products_filter_by_min_price(self):
        response = self.client.get("/api/product/?min_price=100")

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Phone")

    def test_get_products_filter_by_price_range(self):
        response = self.client.get("/api/product/?min_price=40&max_price=60")

        self.assertEqual(len(response.data), 2)

    def test_get_products_filter_by_brand(self):
        response = self.client.get("/api/product/?brand=Amul")

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Milk")

    def test_get_products_filter_by_name(self):
        response = self.client.get("/api/product/?name=bread")

        self.assertEqual(len(response.data), 1)

    def test_get_products_invalid_min_price_returns_400(self):
        response = self.client.get("/api/product/?min_price=notanumber")

        self.assertEqual(response.status_code, 400)


class TestProductCreateAPI(IntegrationTestBase):

    def test_create_product_returns_201(self):
        payload = {
            "name": "Butter",
            "brand": "Amul",
            "price": 60,
            "quantity": 50
        }
        response = self.client.post("/api/product/", payload, format="json")

        self.assertEqual(response.status_code, 201)

    def test_create_product_actually_saves_to_database(self):
        payload = {
            "name": "Butter",
            "brand": "Amul",
            "price": 60,
            "quantity": 50
        }
        self.client.post("/api/product/", payload, format="json")

        product = Product.objects(name="Butter").first()
        self.assertIsNotNone(product)
        self.assertEqual(product.brand, "Amul")

    def test_create_product_missing_required_field_returns_400(self):
        payload = {
            "name": "Butter"
        }
        response = self.client.post("/api/product/", payload, format="json")

        self.assertEqual(response.status_code, 400)

    def test_create_product_response_contains_correct_data(self):
        payload = {
            "name": "Butter",
            "brand": "Amul",
            "price": 60,
            "quantity": 50
        }
        response = self.client.post("/api/product/", payload, format="json")

        self.assertEqual(response.data["name"], "Butter")
        self.assertEqual(response.data["brand"], "Amul")
        self.assertIn("id", response.data) 


class TestProductUpdateAPI(IntegrationTestBase):

    def test_update_product_returns_202(self):
        payload = {
            "name": "Milk Updated",
            "brand": "Amul",
            "price": 55,
            "quantity": 100
        }
        response = self.client.put(
            f"/api/product/{self.milk.id}/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 202)

    def test_update_product_actually_updates_database(self):
        payload = {
            "name": "Milk Updated",
            "brand": "Amul",
            "price": 55,
            "quantity": 100
        }
        self.client.put(
            f"/api/product/{self.milk.id}/",
            payload,
            format="json"
        )

        updated = Product.objects(id=self.milk.id).first()
        self.assertEqual(updated.name, "Milk Updated")
        self.assertEqual(updated.price, 55)

    def test_update_nonexistent_product_returns_404(self):
        payload = {
            "name": "Ghost",
            "brand": "Nobody",
            "price": 0,
            "quantity": 0
        }
        response = self.client.put(
            "/api/product/000000000000000000000000/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 404)


class TestProductDeleteAPI(IntegrationTestBase):

    def test_delete_product_returns_204(self):
        response = self.client.delete(f"/api/product/{self.milk.id}/")

        self.assertEqual(response.status_code, 204)

    def test_delete_product_actually_removes_from_database(self):
        self.client.delete(f"/api/product/{self.milk.id}/")

        deleted = Product.objects(id=self.milk.id).first()
        self.assertIsNone(deleted)

    def test_delete_nonexistent_product_returns_404(self):
        response = self.client.delete("/api/product/000000000000000000000000/")

        self.assertEqual(response.status_code, 404)