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


class ProductCategoryAPITest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super(ProductCategoryAPITest, cls).setUpClass()

        seed()
        cls.client = APIClient()

    
    @classmethod
    def tearDownClass(cls):
        Product.drop_collection()
        ProductCategory.drop_collection()
        disconnect()
        super(ProductCategoryAPITest, cls).tearDownClass()


    def test_list_categories_success(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        products = data.get("results", data)
        self.assertIsInstance(products, list)
        self.assertGreaterEqual(len(products), 0)
        # print("List Products (Success):", products)


    def test_create_category_success(self):
        payload = {
            "title": "New Test Category",
            "description": "Created via integration test"
        }

        url = reverse("category-list")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["title"], payload["title"])
        # print("Create Product (Success):", data)

    
    def test_create_category_invalid_data(self):
        # Missing title
        payload = {"description": "Category with no title"}

        url = reverse("category-list")
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print("Create Category(Failure):", response.json())


    @patch('product.services.product_category.ProductCategoryService.create_category')
    def test_create_product_category_server_error(self, mock_create_product_category):
        mock_create_product_category.side_effect = Exception("Test error")
        payload = {
            "title": "Test title", 
            "description": "Test description"
        }
        url = reverse("category-list")
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Test error")

        # print("Create Product (Server Error):", response_data)


    def test_retrieve_product_category_success(self):
        category = ProductCategory.objects.first()
        url = reverse("category-detail", kwargs = {"pk": str(category.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["title"], category.title)
        # print("Retrieve ProductCategory(success):", data)
    
    
    def test_retrieve_nonexistent_product_category(self):
        fake_id = '67de38ba07c4e845bfd225a8'
        url = reverse("category-detail", kwargs={"pk":fake_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Retrieve Product Category(Failure): ", response.json())

    
    def test_update_product_category_success(self):
        category = ProductCategory.objects.first()
        payload = {
            "title": "Updated title",
            "description": "Updated description"
        }
        url = reverse("category-detail", kwargs={"pk": str(category.id)})
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["title"], payload["title"])
        # print("Update Product Category (Success):", data)


    def test_update_product_category_invalid_data(self):
        category = Product.objects.first()
        # invalid payload 
        payload = {
            "title": " ",
            "description": category.description
        }
        url = reverse("category-detail", kwargs={"pk": str(category.id)})
        # print("Url is ", url)
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        # print("Update Product Category(Failure): ", data)


    def test_update_product_not_found(self):
        fake_id='67de38ba07c4e845bfd225a8'
        payload = {
            "title": "Updated title",
            "description": "updation test"
        }
        url = reverse("category-detail", kwargs={"pk": fake_id})
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # print("Update Product Category Not found ", response.json())


    def test_delete_product_category_success(self):
        # Create a product to delete.
        category_to_delete = ProductCategory(
            title="Category to be deleted",
            description="This product will be deleted"
        )
        category_to_delete.save()
        url = reverse("category-detail", kwargs={"pk": str(category_to_delete.id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(Product.objects(id=category_to_delete.id).first())
        # print("Delete Product (Success): Product deleted successfully.")


    def test_delete_nonexistent_product_category(self):
        fake_id = '67de38ba07c4e845bfd225a8'
        url = reverse("category-detail", kwargs = {"pk": fake_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # print("Delete Product Category(Failure): ", response.json())



    def test_category_products_success(self):
        category = ProductCategory.objects.first()
        url = reverse("category-products", kwargs={"pk": str(category.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = response.json()
        self.assertIsInstance(products, list)
        print("Category Products (Success):", products)



    @patch('product.services.product_category.ProductCategoryService.list_products_in_category')
    def test_category_products_success(self, mock_list_products_in_category):
        mock_list_products_in_category.side_effect = Exception("Test Error")
        category = ProductCategory.objects.first()
        url = reverse("category-products", kwargs={"pk": str(category.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertEqual("Test Error", response_data["error"])


    @patch('product.controllers.product_category.ProductCategoryService.list_products_in_category')
    def test_category_products_failure(self, mock_list_service):
        """
        Test that if the service raises an exception when listing products,
        the API returns a 500 Internal Server Error with the exception message.
        """
        mock_list_service.side_effect = Exception("Test list error")
        category = ProductCategory.objects.first()
        url = reverse("category-products", kwargs={"pk": str(category.id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data.get("error"), "Test list error")
        print("Category Products (Failure):", response.data)

    def test_add_product_to_category_success(self):
        category = ProductCategory.objects.first()
        new_product = Product(
            name="Product To Add",
            description="Product to add via integration test",
            price=79.99,
            brand="AddBrand",
            quantity=30
        )
        new_product.save()
        payload = {"product_id": str(new_product.id)}
        url = reverse("category-add-product", kwargs={"pk": str(category.id)})
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = Product.objects(id=new_product.id).first()
        self.assertIsNotNone(updated_product.category)
        self.assertEqual(str(updated_product.category.id), str(category.id))
        print("Add Product to Category (Success): Product added.")



    def test_add_product_to_category_missing_product_id(self):
        """
        Test that if the product_id is missing in the request,
        the API returns a 400 Bad Request with the proper error message.
        """
        category = ProductCategory.objects.first()
        url = reverse("category-add-product", kwargs={"pk": str(category.id)})
        # Sending an empty payload (no product_id)
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "product id is required.")
        print("Add Product Missing Product ID (Failure):", response.data)



    @patch('product.controllers.product_category.ProductCategoryService.add_product_to_category')
    def test_add_product_to_category_server_error(self, mock_add_service):
        """
        Test that if the service raises an exception during add_product,
        the API returns a 500 Internal Server Error with the exception message.
        """
        mock_add_service.side_effect = Exception("Test add error")
        category = ProductCategory.objects.first()
        url = reverse("category-add-product", kwargs={"pk": str(category.id)})
        product = Product(
                name="Temp Product",
                description="Temp",
                price=10.0,
                brand="TempBrand",
                quantity=10,
                category=category
                )        
      
        product.save()
        payload = {"product_id": str(product.id)}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.json())
        self.assertEqual(response.data.get("error"), "Test add error")
        print("Add Product Server Error (Failure):", response.data)





    def test_remove_product_from_category_success(self):
        # Create a product assigned to a category.
        category = ProductCategory.objects.first()
        product = Product(
            name="Product To Remove",
            description="Product to remove via integration test",
            price=59.99,
            brand="RemoveBrand",
            quantity=20,
            category=category
        )
        product.save()
        payload = {"product_id": str(product.id)}
        url = reverse("category-remove-product", kwargs={"pk": str(category.id)})
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = Product.objects(id=product.id).first()
        self.assertTrue(updated_product.category is None or str(updated_product.category.id) != str(category.id))
        # print("Remove Product from Category (Success): Product removed.")
     


    def test_remove_product_from_category_missing_product_id(self):
        """
        Test that if product_id is missing in the request,
        the API returns a 400 Bad Request with the appropriate error.
        """
        category = ProductCategory.objects.first()
        url = reverse("category-remove-product", kwargs={"pk": str(category.id)})
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())
        self.assertEqual(response.data.get("error"), "product_id is required.")
        print("Remove Product Missing Product ID (Failure):", response.data)

    @patch('product.controllers.product_category.ProductCategoryService.remove_product_from_category')
    def test_remove_product_from_category_server_error(self, mock_remove_service):
        """
        Test that if the service raises an exception during remove_product,
        the API returns a 500 Internal Server Error with the exception message.
        """
        mock_remove_service.side_effect = Exception("Test remove error")
        category = ProductCategory.objects.first()
        url = reverse("category-remove-product", kwargs={"pk": str(category.id)})

        product = Product(
            name="Temp Product",
            description="Temp",
            price=10.0,
            brand="TempBrand",
            quantity=10,
            category=category
        )
        product.save()
        payload = {"product_id": str(product.id)}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
        self.assertEqual(response.data.get("error"), "Test remove error")
        print("Remove Product Server Error (Failure):", response.data)

    # # ----- Test for products (list products in a category) failure scenario -----


if __name__=='__main__':
    unittest.main(verbosity=2)

