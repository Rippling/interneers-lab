import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
import django
django.setup()

import unittest
from unittest.mock import MagicMock, patch
from product.services.product import ProductService

# Your test class and methods follow
class TestProductService(unittest.TestCase):
    @patch("product.services.product.ProductRepository", autospec=True)
    def setUp(self, mock_repo_class):
        self.mock_repo = MagicMock()
        mock_repo_class.return_value = self.mock_repo
        self.product_service = ProductService()

    def test_create_product_success(self):
        data = {'name': 'Test product', 'price': 12}
        mock_product = MagicMock()
        self.mock_repo.create_product.return_value = mock_product
        product = self.product_service.create_product(data)
        self.mock_repo.create_product.assert_called_once_with(data)
        self.assertEqual(product, mock_product)

    def test_create_product_missing_fields(self):
        data = {'price': 10}
        with self.assertRaises(ValueError):
            self.product_service.create_product(data)
        data = {'name': 'Test'}
        with self.assertRaises(ValueError):
            self.product_service.create_product(data)

    def test_get_product_success(self):
        product_id = '123'
        mock_product = MagicMock()
        self.mock_repo.get_product.return_value = mock_product
        product = self.product_service.get_product(product_id)
        self.mock_repo.get_product.assert_called_once_with(product_id)
        self.assertEqual(product, mock_product)

    def test_get_product_not_found(self):
        product_id = '123'
        self.mock_repo.get_product.return_value = None
        with self.assertRaises(ValueError):
            self.product_service.get_product(product_id)
    
    def test_get_all_products_success(self):
        mock_products = MagicMock()
        self.mock_repo.get_all_products.return_value = mock_products
        products = self.product_service.get_all_products()
        self.mock_repo.get_all_products.assert_called_once()
        self.assertEqual(products, mock_products)

    def test_update_product_success(self):
        product_id = '123'
        data = {'price' : 13}
        mock_product = MagicMock()
        self.mock_repo.update_product.return_value = mock_product
        product = self.product_service.update_product(product_id, data)
        self.mock_repo.update_product.assert_called_once_with(product_id, data)
        self.assertEqual(product, mock_product)
    
    def test_update_product_not_found(self):
        product_id = '123'
        data = {'price': 23}
        self.mock_repo.update_product.return_value =None
        with self.assertRaises(ValueError):
            self.product_service.update_product(product_id, data)
        
    def test_delete_product_success(self):
        product_id = '123'
        mock_product = MagicMock()
        self.mock_repo.delete_product.return_value = mock_product
        product = self.product_service.delete_product(product_id)
        self.mock_repo.delete_product.assert_called_once_with(product_id)
        self.assertEqual(product, mock_product)

    def test_delete_product_not_found(self):
        product_id = '123'
        self.mock_repo.delete_product.return_value = None
        with self.assertRaises(ValueError):
            self.product_service.delete_product(product_id)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
