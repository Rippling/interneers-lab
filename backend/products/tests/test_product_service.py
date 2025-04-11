import unittest
from unittest.mock import Mock
from decimal import Decimal

from products.services.product_service import ProductService
from products.repositories.product_repository import ProductDetail


class TestProductService(unittest.TestCase):
    def setUp(self):
        self.repository = Mock()
        self.service = ProductService(self.repository)
        self.mock_products = [
            # BrandA products (2 items)
            ProductDetail(
                name="Wireless Mouse",
                id="1",
                description="Ergonomic mouse",
                price=49.99,
                category="Electronics",
                brand="BrandA",
                quantity=50,
            ),
            ProductDetail(
                name="Mechanical Keyboard",
                id="2",
                description="RGB keyboard",
                price=129.99,
                category="Electronics",
                brand="BrandA",
                quantity=25,
            ),
            # Clothing category (2 items)
            ProductDetail(
                name="Cotton T-Shirt",
                id="3",
                description="Plain cotton t-shirt",
                price=29.99,
                category="Clothing",
                brand="BrandB",
                quantity=100,
            ),
            ProductDetail(
                name="Jeans",
                id="4",
                description="Slim fit jeans",
                price=89.99,
                category="Clothing",
                brand="BrandC",
                quantity=40,
            ),
            # Home Appliances (1 item)
            ProductDetail(
                name="Blender",
                id="5",
                description="High-speed blender",
                price=89.99,
                category="Home Appliances",
                brand="BrandB",
                quantity=15,
            ),
        ]

    def test_get_all_products(self):
        self.repository.get_all_products.return_value = self.mock_products

        products = self.service.get_all_products()

        self.assertEqual(products, self.mock_products)
        self.assertEqual(len(products), 5)
        self.repository.get_all_products.assert_called_once()

    def test_get_all_products_with_filters(self):
        self.repository.get_all_products.return_value = self.mock_products

        filters = {
            "category": "Electronics",
            "name": "Mouse",
            "brand": "BrandA",
            "min_price": 20.00,
            "max_price": 100.00,
        }

        products = self.service.get_all_products(filters=filters)

        # Check if the products returned match the filters
        for product in products:
            self.assertIn(product.category, ["Electronics"])
            self.assertIn("Mouse", product.name)
            self.assertIn("BrandA", product.brand)
            self.assertGreaterEqual(product.price, Decimal(20.00))
            self.assertLessEqual(product.price, Decimal(100.00))

    # Tests for invalid filters
    def test_get_all_products_invalid_min_price(self):
        self.repository.get_all_products.return_value = self.mock_products

        filters = {
            "min_price": "invalid",
        }

        with self.assertRaises(ValueError):
            self.service.get_all_products(filters=filters)

    def test_get_all_products_invalid_max_price(self):
        self.repository.get_all_products.return_value = self.mock_products

        filters = {
            "max_price": "invalid",
        }

        with self.assertRaises(ValueError):
            self.service.get_all_products(filters=filters)

    def test_no_matching_filters(self):
        filters = {"category": "Furniture", "brand": "UnknownBrand"}

        self.repository.get_all_products.return_value = []
        products = self.service.get_all_products(filters=filters)

        self.assertEqual(products, [])

    # Tests for CRUD operations

    def test_get_product_by_id_valid(self):
        mock_product = self.mock_products[0]
        self.repository.get_product_by_id.return_value = mock_product

        product = self.service.get_product_by_id("1")
        self.assertEqual(product, mock_product)
        self.repository.get_product_by_id.assert_called_once_with("1")

    def test_get_product_by_id_not_found(self):
        self.repository.get_product_by_id.side_effect = ValueError("Product not found")

        with self.assertRaises(ValueError) as context:
            self.service.get_product_by_id("999")

        self.assertEqual(str(context.exception), "Product not found")
        self.repository.get_product_by_id.assert_called_once_with("999")

    def test_create_product(self):
        mock_product = ProductDetail(
            name="New Product",
            description="New product description",
            price=99.99,
            category="Electronics",
            brand="BrandA",
            quantity=10,
        )
        self.repository.create_product.return_value = mock_product

        created_product = self.service.create_product(mock_product)

        self.assertEqual(created_product, mock_product)
        self.repository.create_product.assert_called_once_with(mock_product)

    def test_update_product(self):
        mock_product = ProductDetail(
            name="Updated Product",
            description="Updated product description",
            price=79.99,
            category="Electronics",
            brand="BrandA",
            quantity=5,
        )
        self.repository.update_product.return_value = mock_product

        updated_product = self.service.update_product("1", mock_product)

        self.assertEqual(updated_product, mock_product)
        self.repository.update_product.assert_called_once_with("1", mock_product)

    def test_delete_product(self):
        mock_product_id = "1"
        self.repository.delete_product.return_value = True

        result = self.service.delete_product(mock_product_id)

        self.assertTrue(result)
        self.repository.delete_product.assert_called_once_with(mock_product_id)


if __name__ == "__main__":
    unittest.main()
