from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from mongoengine import connect, disconnect
from products.models import ProductCategory
from products.tests.scripts.product_seeds import seed_product_categories


class ProductCategoryApiIntegrationTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        # Set up test database connection
        disconnect()
        connect(
            db="test_product_db", host="mongodb://localhost:27017/", alias="default"
        )
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        # Clean up test database
        from mongoengine.connection import get_connection

        conn = get_connection()
        conn.drop_database("test_product_db")
        disconnect()
        super().tearDownClass()

    def setUp(self):
        ProductCategory.objects.all().delete()
        seed_product_categories()
        self.collection_url = reverse("product-categories")
        self.detail_url = reverse("product-category-detail", args=[1])

    # Test for GET /categories

    def test_get_all_product_categories(self):
        """Test to get all product categories with pagination"""
        # Page 1
        response = self.client.get(self.collection_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], 7)

        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])
        self.assertEqual(len(response.data["results"]), 5)  # Default page size = 5

        # Page 2
        response_page2 = self.client.get(self.collection_url, {"page": 2})
        self.assertEqual(response_page2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_page2.data["count"], 7)

        self.assertIsNone(response_page2.data["next"])
        self.assertIn(
            response_page2.data["previous"],
            [
                f"http://testserver{self.collection_url}",
                f"http://testserver{self.collection_url}?page=1",
            ],
        )

        self.assertEqual(len(response_page2.data["results"]), 2)

    # Test for POST /categories

    def test_create_product_category(self):
        """Test to create a new product category"""
        data = {"title": "New Category", "description": "Description for new category"}
        response = self.client.post(self.collection_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        category = ProductCategory.objects(title="New Category").first()
        self.assertIsNotNone(category)

    # Tests for GET /categories/{id}

    def test_get_product_category_by_id(self):
        """Test retrieving a single product category by ID"""
        category = ProductCategory.objects.first()
        response = self.client.get(
            reverse("product-category-detail", args=[str(category.id)])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], category.title)

    def test_get_product_category_invalid_id(self):
        """Test retrieving category with an invalid ID"""
        response = self.client.get(
            reverse("product-category-detail", args=["invalid123"])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # Tests for PUT /categories/{id}

    def test_update_product_category(self):
        """Test updating a product category"""
        category = ProductCategory.objects.first()
        data = {"title": "Updated title", "description": "Updated description"}
        response = self.client.put(
            reverse("product-category-detail", args=[str(category.id)]),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_invalid_data(self):
        """Test updating with invalid data"""
        category = ProductCategory.objects.first()
        data = {"title": ""}  # title shouldn't be empty
        response = self.client.put(
            reverse("product-category-detail", args=[str(category.id)]),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_put_update_nonexistent_category(self):
        """Test update of a non-existent category"""
        fake_id = "6440e0d8f0d4f7a0c0e0f0f0"  # some MongoDB ObjectId-like string
        data = {"title": "New Title"}
        response = self.client.put(
            reverse("product-category-detail", args=[fake_id]), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_put_update_with_empty_body(self):
        """Test update with empty payload"""
        category = ProductCategory.objects.first()
        response = self.client.put(
            reverse("product-category-detail", args=[str(category.id)]),
            data={},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)

    # Tests for DELETE /categories/{id}
    def test_delete_product_category_success(self):
        """Test deleting a product category"""
        category = ProductCategory.objects.first()

        response = self.client.delete(
            reverse("product-category-detail", args=[str(category.id)])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["message"], "Category deleted successfully")

        self.assertIsNone(ProductCategory.objects(id=category.id).first())

    def test_delete_nonexistent_product_category(self):
        """Test deleting a category that doesn't exist"""
        fake_id = "6440e0d8f0d4f7a0c0e0f0f0"

        response = self.client.delete(
            reverse("product-category-detail", args=[fake_id])
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
