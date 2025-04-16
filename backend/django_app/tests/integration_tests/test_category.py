import unittest
from django.test import Client
import json


class TestProductCategoryIntegration(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = "/categories/"

    def test_create_category(self):
        data = {
            "title": "Electronics",
            "description": "Gadgets and devices"
        }
        response = self.client.post(f"{self.base_url}create/", json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_get_category(self):
        # First, create a category
        data = {
            "title": "Electronics",
            "description": "Gadgets and devices"
        }
        create_response = self.client.post(f"{self.base_url}create/", json.dumps(data), content_type="application/json")
        category_id = create_response.json()["id"]

        # Fetch the created category
        response = self.client.get(f"{self.base_url}{category_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Electronics")

    def test_list_categories(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_update_category(self):
        # First, create a category
        data = {
            "title": "Electronics",
            "description": "Gadgets and devices"
        }
        create_response = self.client.post(f"{self.base_url}create/", json.dumps(data), content_type="application/json")
        category_id = create_response.json()["id"]

        # Update the category
        update_data = {"description": "Updated description"}
        response = self.client.put(
            f"{self.base_url}{category_id}/update/",
            json.dumps(update_data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Category updated successfully")

    def test_delete_category(self):
        # First, create a category
        data = {
            "title": "Electronics",
            "description": "Gadgets and devices"
        }
        create_response = self.client.post(f"{self.base_url}create/", json.dumps(data), content_type="application/json")
        category_id = create_response.json()["id"]

        # Delete the category
        response = self.client.delete(f"{self.base_url}{category_id}/delete/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Category deleted successfully")


if __name__ == '__main__':
    unittest.main()
