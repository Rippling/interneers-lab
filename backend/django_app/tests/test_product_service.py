import unittest
from unittest.mock import patch
from django_app.services import ProductService
from django_app.repository import ProductRepository

class MockDocument:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data

class TestProductService(unittest.TestCase):

    @patch.object(ProductRepository, 'create_product')
    def test_create_product(self, mock_create_product):
        mock_create_product.return_value = MockDocument({
            "id": "1234",
            "name": "iPhone",
            "description": "Great camera and performance",
            "category": {"title": "Electronics"},
            "price": 70000,
            "brand": "Apple",
            "quantity": 5,
        })
        data = {
            "name": "iPhone",
            "description": "Great camera and performance",
            "category": "Electronics",
            "price": 70000,
            "brand": "Apple",
            "quantity": 5,
        }
        product = ProductService.create_product(data)
        self.assertEqual(product["name"], "iPhone")
        self.assertEqual(product["brand"], "Apple")

    @patch.object(ProductRepository, 'get_product_by_id')
    def test_get_product(self, mock_get_product):
        mock_get_product.return_value = MockDocument({
            "id": "1234",
            "name": "iPhone",
            "description": "Great camera and performance",
        })
        product = ProductService.get_product("1234")
        self.assertEqual(product["id"], "1234")

    @patch.object(ProductRepository, 'update_product')
    def test_update_product(self, mock_update_product):
        mock_update_product.return_value = 1
        data = {"price": 75000}
        result = ProductService.update_product("1234", data)
        self.assertEqual(result, 1)

    @patch.object(ProductRepository, 'delete_product')
    def test_delete_product(self, mock_delete_product):
        mock_delete_product.return_value = 1
        result = ProductService.delete_product("1234")
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
