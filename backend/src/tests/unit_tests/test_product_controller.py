"""
Unit tests for the product endpoint module.

This module verifies CRUD functionality, pagination behavior, and validation checks
for the /product endpoint in the Django application.
"""

import json
from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from src.controllers.product_controller import product_endpoint
from src.models.product import Product
from mongoengine.errors import DoesNotExist

class ProductEndpointTests(TestCase):
    """
    TestCase class for testing the /product API endpoint.

    Covers functionality for GET, POST, PATCH, and DELETE requests,
    along with validation and pagination.
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.valid_product = {
            "name": "Sample Product",
            "price": 100,
            "quantity": 10,
            "details": "Sample details"
        }

    @patch("src.controllers.product_controller.Product.objects")
    def test_get_product_by_id_success(self, mock_objects):
        """Test retrieving a product by valid ID returns 200 and correct data."""
        mock_product = MagicMock()
        mock_product.to_json.return_value = json.dumps(self.valid_product)
        mock_objects.get.return_value = mock_product

        request = self.factory.get("/product/1")
        response = product_endpoint(request, "1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), self.valid_product)

    @patch("src.controllers.product_controller.Product.objects")
    def test_get_product_by_invalid_id(self, mock_objects):
        """Test retrieving a non-existent product returns 404."""
        mock_objects.get.side_effect = DoesNotExist

        request = self.factory.get("/product/999")
        response = product_endpoint(request, "999")

        self.assertEqual(response.status_code, 404)

    @patch("src.controllers.product_controller.create_product")
    def test_post_product_success(self, mock_create):
        """Test creating a product with valid data returns 201 and saves the product."""
        mock_product = MagicMock()
        mock_product.to_json.return_value = json.dumps(self.valid_product)
        mock_product.id = "1"
        mock_product.save = MagicMock()
        mock_create.return_value = mock_product

        request = self.factory.post(
            "/product",
            data=json.dumps(self.valid_product),
            content_type="application/json"
        )

        response = product_endpoint(request)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Location", response.headers)
        self.assertEqual(json.loads(response.content), self.valid_product)

    def test_post_invalid_product_missing_name(self):
        """Test creating product with missing name returns 400."""
        invalid_data = {
            "price": 100,
            "quantity": 10
        }

        request = self.factory.post(
            "/product",
            data=json.dumps(invalid_data),
            content_type="application/json"
        )
        response = product_endpoint(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.content.decode())

    def test_post_invalid_product_price_type(self):
        """Test creating product with string price returns 400."""
        invalid_data = {
            "name": "Item",
            "price": "free",
            "quantity": 1
        }

        request = self.factory.post(
            "/product",
            data=json.dumps(invalid_data),
            content_type="application/json"
        )
        response = product_endpoint(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("price", response.content.decode())

    @patch("src.controllers.product_controller.Product.objects")
    def test_patch_update_product(self, mock_objects):
        """Test updating product fields returns 204 and saves the updated product."""
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_product.save = MagicMock()
        mock_objects.get.return_value = mock_product

        request = self.factory.patch(
            "/product/1",
            data=json.dumps({"price": 200}),
            content_type="application/json"
        )

        response = product_endpoint(request, "1")
        self.assertEqual(response.status_code, 204)

    @patch("src.controllers.product_controller.Product.objects")
    def test_patch_update_with_id_field_should_fail(self, mock_objects):
        """Test attempting to update product ID returns 400."""
        mock_product = MagicMock()
        mock_product.id = "1"
        mock_objects.get.return_value = mock_product

        request = self.factory.patch(
            "/product/1",
            data=json.dumps({"id": "999"}),
            content_type="application/json"
        )

        response = product_endpoint(request, "1")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Product ID cannot be updated", response.content.decode())

    @patch("src.controllers.product_controller.Product.objects")
    def test_patch_product_not_found(self, mock_objects):
        """Test updating non-existent product returns 404."""
        mock_objects.get.side_effect = DoesNotExist

        request = self.factory.patch(
            "/product/999",
            data=json.dumps({"price": 100}),
            content_type="application/json"
        )
        response = product_endpoint(request, "999")

        self.assertEqual(response.status_code, 404)

    @patch("src.controllers.product_controller.Product.objects")
    def test_delete_product_success(self, mock_objects):
        """Test successful deletion of product returns 204."""
        mock_product = MagicMock()
        mock_objects.get.return_value = mock_product

        request = self.factory.delete("/product/1")
        response = product_endpoint(request, "1")

        self.assertEqual(response.status_code, 204)

    @patch("src.controllers.product_controller.Product.objects")
    def test_delete_product_not_found(self, mock_objects):
        """Test deleting non-existent product returns 404."""
        mock_objects.get.side_effect = DoesNotExist

        request = self.factory.delete("/product/404")
        response = product_endpoint(request, "404")

        self.assertEqual(response.status_code, 404)

    @patch("src.controllers.product_controller.Product.objects")
    def test_get_paginated_products(self, mock_objects):
        """Test fetching paginated products returns 206 with data and navigation."""
        mock_objects.count.return_value = 3
        mock_qs = MagicMock()
        mock_qs.to_json.return_value = json.dumps([
            self.valid_product,
            self.valid_product,
            self.valid_product
        ])
        mock_objects.__getitem__.return_value = mock_qs

        request = self.factory.get("/product?start=0&limit=2")
        response = product_endpoint(request)

        self.assertEqual(response.status_code, 206)
        data = json.loads(response.content)
        self.assertIn("data", data)
        self.assertIn("navigation", data)

    def test_get_paginated_invalid_start_param(self):
        """Test invalid start param returns 400."""
        request = self.factory.get("/product?start=abc")
        response = product_endpoint(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("start", response.content.decode())

    def test_get_paginated_invalid_limit_param(self):
        """Test invalid limit param returns 400."""
        request = self.factory.get("/product?limit=xyz")
        response = product_endpoint(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("limit", response.content.decode())

    def test_get_paginated_limit_too_large(self):
        """Test exceeding max limit param returns 400."""
        request = self.factory.get("/product?limit=300")
        response = product_endpoint(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn("limit", response.content.decode())

    def test_invalid_method(self):
        """Test unsupported HTTP method returns 405."""
        request = self.factory.put("/product")
        response = product_endpoint(request)
        self.assertEqual(response.status_code, 405)
