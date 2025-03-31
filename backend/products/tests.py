from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

# Import the in-memory products list
from products.views import products  

class ProductTests(TestCase):
    
    def setUp(self):
        """Initialize test client and add a product."""
        self.client = APIClient()
        products.clear()  # Clear any existing products
        self.product_data = {
            "id": 4,
            "name": "Test Product",
            "price": 99.99,

        }
        products.append(self.product_data)  # Manually add the product

    def test_get_product(self):
        """Test getting a product."""
        response = self.client.get("/api/products/4/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Product")

    def test_update_product(self):
        """Test updating a product."""
        update_data = {"price": 150.00}
        response = self.client.put("/api/products/4/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], 150.00)

    def test_delete_product(self):
        """Test deleting a product."""
        response = self.client.delete("/api/products/4/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        


    
        

    

# Create your tests here.
