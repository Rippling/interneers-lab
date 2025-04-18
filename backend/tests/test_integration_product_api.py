import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
import django
django.setup()

import unittest
from mongoengine import connect, disconnect
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from product.models.product import Product
from product.models.product_category import ProductCategory
from product.seed_data_test import seed
from unittest.mock import patch


class ProductAPITest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(ProductAPITest, cls).setUpClass()

        seed()
        cls.client = APIClient()

    
    @classmethod
    def tearDownClass(cls):
        Product.drop_collection()
        ProductCategory.drop_collection()
        disconnect()
        super(ProductAPITest, cls).tearDownClass()


    def test_list_products_success(self):
        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        products = data.get("results", data)
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 0)
        # print("List Products (Success):", products)


    def test_create_product_success(self):
        category = ProductCategory.objects.first()
        payload = {
            "name": "New Integration Product",
            "description": "Created via integration test",
            "price": 79.99,
            "brand": "NewBrand",
            "quantity": 15,
            "category": str(category.id)
        }
        url = reverse("product-list")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["name"], payload["name"])
        # print("Create Product (Success):", data)

    
    def test_create_product_invalid_data(self):
        # Missing required fields: "name" and "price"
        payload = {
            "description": "Created via integration test",
            "brand": "NewBrand",
            "quantity": 15,
        }

        url = reverse("product-list")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # print("Create Product(Failure):", response.json())


    @patch('product.services.product.ProductService.create_product')
    def test_create_product_server_error(self, mock_create_product):
        mock_create_product.side_effect = Exception("Test error")
        category = ProductCategory.objects.first()
        payload = {
            "name": "New Integration Product",
            "description": "Created via integration test",
            "price": 79.99,
            "brand": "NewBrand",
            "quantity": 15,
            "category": str(category.id)
        }
        url = reverse("product-list")
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Test error")

        # print("Create Product (Server Error):", response_data)


    def test_retrieve_product_success(self):
        product = Product.objects.first()
        url = reverse("product-detail", kwargs = {"pk": str(product.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], product.name)
        # print("Retrieve Product(success):", data)
    
    
    def test_retrieve_nonexistent_product(self):
        fake_id = '67de38ba07c4e845bfd225a8'
        url = reverse("product-detail", kwargs={"pk":fake_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # print("Retrieve Product (Failure): ", response.json())

    
    def test_update_product_success(self):
        product = Product.objects.first()
        payload = {
            "name": "Updated Product",
            "description": product.description,
            "price": 243,
            "brand": product.brand,
            "quantity": product.quantity,
            "category": str(product.category.id) if product.category else None
        }
        url = reverse("product-detail", kwargs={"pk": str(product.id)})
        print("Url is ", url)
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # self.assertEqual(data["name"], payload["name"])
        # print("Update Product (Success):", data)


    def test_update_product_invalid_data(self):
        product = Product.objects.first()
        # invalid price 
        payload = {
            "name": "Updated Product",
            "description": product.description,
            "price": 323243,
            "brand": product.brand,
            "quantity": product.quantity,
            "category": str(product.category.id) if product.category else None
        }
        url = reverse("product-detail", kwargs={"pk": str(product.id)})
        # print("Url is ", url)
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        # print("Update Product (Failure): ", response.json())


    def test_update_product_not_found(self):
        fake_id='67de38ba07c4e845bfd225a8'
        payload = {
            "name": "Updated Product",
            "description": "updation test",
            "brand": "test",
            "price": 32
        }
        url = reverse("product-detail", kwargs={"pk": fake_id})
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # print("Update Product Not found ", response.json())


    def test_delete_product_success(self):
        # Create a product to delete.
        category = ProductCategory.objects.first()
        product_to_delete = Product(
            name="Product To Delete",
            description="This product will be deleted",
            price=59.99,
            brand="DeleteBrand",
            quantity=5,
            category=category
        )
        product_to_delete.save()
        url = reverse("product-detail", kwargs={"pk": str(product_to_delete.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Product.objects(id=product_to_delete.id).first())
        print("Delete Product (Success): Product deleted successfully.")


    def test_delete_nonexistent_product(self):
        fake_id = '67de38ba07c4e845bfd225a8'
        url = reverse("product-detail", kwargs = {"pk": fake_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Delete Product (Failure): ", response.json())

    
if __name__=='__main__':
    unittest.main(verbosity=2)