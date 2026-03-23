from productAPI.models import ProductCategory
from productAPI.tests.integration_test_base import IntegrationTestBase


class TestCategoryListAPI(IntegrationTestBase):

    def test_get_all_categories_returns_200(self):
        response = self.client.get("/api/categories/")

        self.assertEqual(response.status_code, 200)

    def test_get_all_categories_returns_correct_count(self):
        response = self.client.get("/api/categories/")

        self.assertEqual(len(response.data), 3)


class TestCategoryCreateAPI(IntegrationTestBase):

    def test_create_category_returns_201(self):
        payload = {
            "title": "Sports",
            "description": "Sports equipment"
        }
        response = self.client.post("/api/categories/", payload, format="json")

        self.assertEqual(response.status_code, 201)

    def test_create_category_saves_to_database(self):
        payload = {
            "title": "Sports",
            "description": "Sports equipment"
        }
        self.client.post("/api/categories/", payload, format="json")

        category = ProductCategory.objects(title="Sports").first()
        self.assertIsNotNone(category)

    def test_create_category_missing_title_returns_400(self):
        payload = {"description": "No title here"}
        response = self.client.post("/api/categories/", payload, format="json")

        self.assertEqual(response.status_code, 400)


class TestCategoryUpdateAPI(IntegrationTestBase):

    def test_update_category_returns_202(self):
        payload = {
            "title": "Food Updated",
            "description": "Updated description"
        }
        response = self.client.put(
            f"/api/categories/{self.food_category.id}/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 202)

    def test_update_category_actually_updates_database(self):
        payload = {
            "title": "Food Updated",
            "description": "Updated description"
        }
        self.client.put(
            f"/api/categories/{self.food_category.id}/",
            payload,
            format="json"
        )

        updated = ProductCategory.objects(id=self.food_category.id).first()
        self.assertEqual(updated.title, "Food Updated")

    def test_update_nonexistent_category_returns_404(self):
        payload = {"title": "Ghost", "description": "..."}
        response = self.client.put(
            "/api/categories/000000000000000000000000/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 404)


class TestCategoryDeleteAPI(IntegrationTestBase):

    def test_delete_category_returns_204(self):
        response = self.client.delete(f"/api/categories/{self.food_category.id}/")

        self.assertEqual(response.status_code, 204)

    def test_delete_category_removes_from_database(self):
        self.client.delete(f"/api/categories/{self.food_category.id}/")

        deleted = ProductCategory.objects(id=self.food_category.id).first()
        self.assertIsNone(deleted)

    def test_delete_nonexistent_category_returns_404(self):
        response = self.client.delete("/api/categories/000000000000000000000000/")

        self.assertEqual(response.status_code, 404)