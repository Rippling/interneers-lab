from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mongoengine import connect, disconnect
from mongoengine.connection import get_connection
from products.models import Product, ProductCategory
from products.tests.scripts.product_seeds import seed_products, seed_product_categories


class ProductApiIntegrationTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect(
            db="test_product_db", host="mongodb://localhost:27017/", alias="default"
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        conn = get_connection()
        conn.drop_database("test_product_db")
        disconnect()
        super().tearDownClass()

    def setUp(self):
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        seed_product_categories()
        seed_products()
        self.collection_url = reverse("products")
        self.detail_url = reverse("product-detail", args=[1])

    # Test for GET /products

    def test_get_all_products(self):
        """Test to get all products with pagination"""
        response = self.client.get(self.collection_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)  # Adjust based on seeded data
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(len(response.data["results"]), 5)  # Default page size = 5

    # Test for GET /products?page=2
    def test_get_all_products_page_2(self):
        """Test to get all products on page 2"""
        response = self.client.get(self.collection_url, {"page": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 10)  # Adjust based on seeded data
        self.assertIsNone(response.data["next"])
        self.assertIn(
            response.data["previous"],
            [
                f"http://testserver{self.collection_url}",
                f"http://testserver{self.collection_url}?page=1",
            ],
        )
        self.assertEqual(len(response.data["results"]), 5)  # Default page size = 5

    # Test for GET /products?category=Electronics
    def test_get_all_products_by_category(self):
        """Test to get all products by category"""
        response = self.client.get(self.collection_url, {"category": "Electronics"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_get_all_products_by_category_invalid(self):
        """Test to get all products by invalid category"""
        response = self.client.get(self.collection_url, {"category": "InvalidCategory"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    # Test for GET /products?name=Smartphone
    def test_get_all_products_by_name(self):
        """Test to get all products by name"""
        response = self.client.get(self.collection_url, {"name": "Smartphone"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    # Test for GET /products?brand=TechMaster
    def test_get_all_products_by_brand(self):
        """Test to get all products by brand"""
        response = self.client.get(self.collection_url, {"brand": "TechMaster"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    # Test for GET /products?min_price=100&max_price=1000
    def test_get_all_products_by_price_range(self):
        """Test to get all products by price range"""
        response = self.client.get(
            self.collection_url, {"min_price": 100, "max_price": 1000}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    # Test for GET /products?min_price=invalid
    def test_get_all_products_invalid_min_price(self):
        """Test to get all products with invalid min_price"""
        response = self.client.get(self.collection_url, {"min_price": "invalid"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test for GET /products?max_price=invalid
    def test_get_all_products_invalid_max_price(self):
        """Test to get all products with invalid max_price"""
        response = self.client.get(self.collection_url, {"max_price": "invalid"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test for GET /products for combined filters
    def test_get_all_products_combined_filters(self):
        """Test to get all products with combined filters"""
        response = self.client.get(
            self.collection_url,
            {
                "category": "Electronics",
                "name": "Smartphone",
                "brand": "TechMaster",
                "min_price": 100,
                "max_price": 1000,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    # Test for GET /products with no matching filters
    def test_get_all_products_no_matching_filters(self):
        """Test to get all products with no matching filters"""
        response = self.client.get(
            self.collection_url, {"category": "Furniture", "brand": "UnknownBrand"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    # Test for GET /products/{id}
    def test_get_product_by_id(self):
        """Test to get a product by ID"""
        product = Product.objects.first()
        response = self.client.get(reverse("product-detail", args=[str(product.id)]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(product.id))

    # Test for GET /products/{id} with invalid ID
    def test_get_product_by_invalid_id(self):
        """Test to get a product by invalid ID"""
        response = self.client.get(reverse("product-detail", args=["invalid123"]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # Test for POST /products
    def test_create_product(self):
        """Test to create a new product"""
        data = {
            "name": "New Product",
            "description": "Description for new product",
            "price": 150.00,
            "category": "Electronics",
            "brand": "BrandX",
            "quantity": 10,
        }
        response = self.client.post(self.collection_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the product was created in the database
        product = Product.objects(name="New Product").first()
        self.assertIsNotNone(product)

    def test_create_product_invalid_data(self):
        """Test to create a product with invalid data"""
        data = {
            "name": "",
            "description": "Description for new product",
            "price": 150.00,
            "category": "Electronics",
            "brand": "BrandX",
            "quantity": 10,
        }
        response = self.client.post(self.collection_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("details", response.data)
        self.assertIn("name", response.data["details"])
        self.assertIn("This field may not be blank.", response.data["details"]["name"])

    # Test for PUT /products/{id}
    def test_update_product(self):
        """Test to update a product"""
        product = Product.objects.first()
        data = {
            "name": "Updated Product",
            "description": "Updated description",
            "price": 200.00,
            "category": "Electronics",
            "brand": "BrandY",
            "quantity": 15,
        }
        response = self.client.put(
            reverse("product-detail", args=[str(product.id)]), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_invalid_data(self):
        """Test to update a product with invalid data"""
        product = Product.objects.first()
        data = {
            "name": "",
            "description": "Updated description",
            "price": 200.00,
            "category": "Electronics",
            "brand": "BrandY",
            "quantity": 15,
        }
        response = self.client.put(
            reverse("product-detail", args=[str(product.id)]), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("details", response.data)
        self.assertIn("name", response.data["details"])
        self.assertIn("This field may not be blank.", response.data["details"]["name"])

    # Test for DELETE /products/{id}
    def test_delete_product(self):
        """Test to delete a product"""
        product = Product.objects.first()
        response = self.client.delete(reverse("product-detail", args=[str(product.id)]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the product was deleted from the database
        product = Product.objects.filter(id=product.id).first()
        self.assertIsNone(product)

    def test_delete_product_invalid_id(self):
        """Test to delete a product with invalid ID"""
        response = self.client.delete(reverse("product-detail", args=["invalid123"]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
