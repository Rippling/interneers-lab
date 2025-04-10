import unittest
from unittest.mock import patch, MagicMock
from products_mongo.product_service import ProductService
from bson import ObjectId
from datetime import datetime


class TestProductService(unittest.TestCase):

    @patch('products_mongo.product_repository.ProductRepository.create')
    def test_create_product(self, mock_create):
        """Test creating a product."""
        mock_product = {"name": "Test Product", "price": 100.00, "brand": "Test Brand"}
        mock_create.return_value = mock_product  # Mock DB response

        result = ProductService.create_product(mock_product)
        self.assertEqual(result, mock_product)
        mock_create.assert_called_once_with(mock_product)

    @patch('products_mongo.product_repository.ProductRepository.get_by_id')
    @patch('products_mongo.product_repository.ProductRepository.format_product')
    def test_get_product_by_id(self, mock_format, mock_get_by_id):
        """Test retrieving a product by ID."""
        mock_product = {"_id": ObjectId(), "name": "Test Product"}
        mock_get_by_id.return_value = mock_product
        mock_format.return_value = {"id": str(mock_product["_id"]), "name": "Test Product"}

        result = ProductService.get_product_by_id(mock_product["_id"])
        self.assertEqual(result, {"id": str(mock_product["_id"]), "name": "Test Product"})
        mock_get_by_id.assert_called_once_with(mock_product["_id"])
        mock_format.assert_called_once_with(mock_product)

    @patch('products_mongo.product_repository.ProductRepository.get_all')
    @patch('products_mongo.product_repository.ProductRepository.format_product')
    def test_get_all_products(self, mock_format, mock_get_all):
        """Test retrieving all products with pagination."""
        mock_products = [
            {"_id": ObjectId(), "name": "Product 1"},
            {"_id": ObjectId(), "name": "Product 2"}
        ]
        mock_get_all.return_value = mock_products
        mock_format.side_effect = lambda x: {"id": str(x["_id"]), "name": x["name"]}

        result = ProductService.get_all_products(page=1, per_page=2)
        expected = [
            {"id": str(mock_products[0]["_id"]), "name": "Product 1"},
            {"id": str(mock_products[1]["_id"]), "name": "Product 2"}
        ]
        self.assertEqual(result, expected)
        mock_get_all.assert_called_once_with(1, 2)

    @patch('products_mongo.product_repository.ProductRepository.update')
    @patch('products_mongo.product_repository.ProductRepository.format_product')
    def test_update_product(self, mock_format, mock_update):
        """Test updating a product."""
        mock_product = {"_id": ObjectId(), "name": "Updated Product"}
        mock_update.return_value = mock_product
        mock_format.return_value = {"id": str(mock_product["_id"]), "name": "Updated Product"}

        result = ProductService.update_product(mock_product["_id"], {"name": "Updated Product"})
        self.assertEqual(result, {"id": str(mock_product["_id"]), "name": "Updated Product"})
        mock_update.assert_called_once_with(mock_product["_id"], {"name": "Updated Product"})

    @patch('products_mongo.product_repository.ProductRepository.delete')
    def test_delete_product(self, mock_delete):
        """Test deleting a product."""
        mock_delete.return_value = True

        result = ProductService.delete_product(ObjectId())
        self.assertTrue(result)
        mock_delete.assert_called_once()
        
    
    @patch('products_mongo.product_repository.ProductRepository.get_by_date_range')
    @patch('products_mongo.product_repository.ProductRepository.format_product')
    def test_get_product_by_date_range(self, mock_format, mock_get_by_date_range):
        """Test retrieving products within a date range."""
        mock_products = [
            {"_id": ObjectId(), "name": "Product 1", "created_at": datetime(2024, 4, 1)},
            {"_id": ObjectId(), "name": "Product 2", "created_at": datetime(2024, 4, 3)}
        ]
        mock_get_by_date_range.return_value = mock_products
        mock_format.side_effect = lambda x: {"id": str(x["_id"]), "name": x["name"], "date": x["created_at"].strftime("%Y-%m-%d")}

        start_date = datetime(2024, 4, 1)
        end_date = datetime(2024, 4, 5)
        result = ProductService.get_product_by_date_range(start_date, end_date)
        
        expected = [
            {"id": str(mock_products[0]["_id"]), "name": "Product 1", "date": "2024-04-01"},
            {"id": str(mock_products[1]["_id"]), "name": "Product 2", "date": "2024-04-03"}
        ]

        self.assertEqual(result, expected)
        mock_get_by_date_range.assert_called_once_with(start_date, end_date)

    @patch('products_mongo.product_service.ProductService.get_products_by_category')
    def test_get_products_by_category(self, mock_get_products_by_category):
        """Test retrieving products by category ID."""
        
        mock_category_id = ObjectId()
        mock_products = [
            {"_id": str(ObjectId()), "name": "Category Product 1"},
            {"_id": str(ObjectId()), "name": "Category Product 2"}
        ]
        mock_get_products_by_category.return_value = mock_products

        # Call the actual service method
        service = ProductService()  # Ensure instance is created
        result = service.get_products_by_category(mock_category_id)

        # Expected output
        expected = [{"_id": str(p["_id"]), "name": p["name"]} for p in mock_products]

        self.assertEqual(result, expected)
        mock_get_products_by_category.assert_called_once_with(mock_category_id)
        

    @patch('products_mongo.product_service.ProductService.add_product_to_category')
    def test_add_product_to_category(self, mock_add_product_to_category):
        """Test adding a product to a category."""
        mock_product_id = ObjectId()
        mock_category_id = ObjectId()
        mock_add_product_to_category.return_value = True  # Simulate success

        result = ProductService.add_product_to_category(mock_product_id, mock_category_id)
        self.assertTrue(result)
        mock_add_product_to_category.assert_called_once_with(mock_product_id, mock_category_id)

    @patch('products_mongo.product_service.ProductService.remove_product_from_category')
    def test_remove_product_from_category(self, mock_remove_product_from_category):
        """Test removing a product from a category."""
        mock_product_id = ObjectId()
        mock_category_id = ObjectId()
        mock_remove_product_from_category.return_value = True  # Simulate success

        result = ProductService.remove_product_from_category(mock_product_id, mock_category_id)
        self.assertTrue(result)
        mock_remove_product_from_category.assert_called_once_with(mock_product_id, mock_category_id)

if __name__ == '__main__':
    unittest.main()
