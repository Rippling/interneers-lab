from productAPI.models import Product
from productAPI.tests.integration_test_base import IntegrationTestBase


class TestCategoryWiseProductListAPI(IntegrationTestBase):

    def test_get_products_by_category_returns_200(self):
        response = self.client.get(f"/api/categories/{self.food_category.id}/products/")

        self.assertEqual(response.status_code, 200)

    def test_get_products_by_category_returns_correct_products(self):
        response = self.client.get(f"/api/categories/{self.food_category.id}/products/")

        self.assertEqual(len(response.data), 2)
        names = [p["name"] for p in response.data]
        self.assertIn("Milk", names)
        self.assertIn("Bread", names)


class TestAssignProductToCategoryAPI(IntegrationTestBase):

    def test_assign_product_to_category_returns_200(self):
        payload = {"id": str(self.phone.id)}
        response = self.client.post(
            f"/api/categories/{self.food_category.id}/products/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 200)

    def test_assign_product_actually_updates_database(self):
        payload = {"id": str(self.phone.id)}
        self.client.post(
            f"/api/categories/{self.food_category.id}/products/",
            payload,
            format="json"
        )

        updated_phone = Product.objects(id=self.phone.id).first()
        self.assertEqual(str(updated_phone.category.id), str(self.food_category.id))

    def test_assign_nonexistent_product_returns_404(self):
        payload = {"id": "000000000000000000000000"}
        response = self.client.post(
            f"/api/categories/{self.food_category.id}/products/",
            payload,
            format="json"
        )

        self.assertEqual(response.status_code, 404)


class TestUnassignProductFromCategoryAPI(IntegrationTestBase):

    def test_unassign_product_returns_204(self):
        response = self.client.delete(
            f"/api/categories/{self.food_category.id}/products/{self.milk.id}/"
        )

        self.assertEqual(response.status_code, 204)

    def test_unassign_product_sets_category_to_null_in_database(self):
        self.client.delete(
            f"/api/categories/{self.food_category.id}/products/{self.milk.id}/"
        )

        updated_milk = Product.objects(id=self.milk.id).first()
        self.assertIsNone(updated_milk.category)

    def test_unassign_nonexistent_product_returns_404(self):
        response = self.client.delete(
            f"/api/categories/{self.food_category.id}/products/000000000000000000000000/"
        )

        self.assertEqual(response.status_code, 404)