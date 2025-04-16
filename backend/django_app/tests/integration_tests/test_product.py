import unittest
from django.test import Client
import json

class TestProductIntegration(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url_products = "/products/"
        self.base_url_categories = "/categories/"

    def test_create_product(self):
        # Create a category first
        category_data = {
            "title": "Electronics",
            "description": "Gadgets and devices"
        }
        create_category_response = self.client.post(
            f"{self.base_url_categories}create/",
            json.dumps(category_data),
            content_type="application/json"
        )
        
        product_data = {
            "name": "iPhone",
            "description": "Great camera and performance",
            "category": "Electronics",
            "price": 70000,
            "brand": "Apple",
            "quantity": 5,
        }
        
        response = self.client.post(
            f"{self.base_url_products}create/",
            json.dumps(product_data),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_get_product(self):
        # Create a product first
        product_data = {
            "name": "iPhone",
            "description": "Great camera and performance",
            "category": "Electronics",
            "price": 70000,
            "brand": "Apple",
            "quantity": 5,
        }
        
        create_response = self.client.post(
            f"{self.base_url_products}create/",
            json.dumps(product_data),
            content_type="application/json"
        )
        
        product_id = create_response.json()["id"]

        # Fetch the created product
        response = self.client.get(f"{self.base_url_products}{product_id}/")
        
        self.assertEqual(response.status_code, 200)
        
    def test_list_products(self):
        
         response=self.client.get('/products/')
         assert isinstance(response.json(),list)