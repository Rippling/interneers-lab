import unittest
from unittest.mock import patch
from django_app.services import ProductCategoryService
from django_app.repository import ProductCategoryRepository

class MockDocument:
    def __init__(self, data):
        self.data = data

    def to_dict(self):
        return self.data

    def __getitem__(self, key):  # Allow dictionary-like access
        return self.data[key]

class TestProductCategoryService(unittest.TestCase):

    @patch.object(ProductCategoryRepository, 'create_category')
    def test_create_category(self, mock_create_category):
        mock_create_category.return_value = MockDocument({
            "id": "5678",
            "title": "Electronics",
            "description": "Gadgets and devices",
        })
        data = {
            "title": "Electronics",
            "description": "Gadgets and devices"
        }
        category = ProductCategoryService.create_category(data)
        self.assertEqual(category["title"], "Electronics")

    @patch.object(ProductCategoryRepository, 'get_category_by_id')
    def test_get_category(self, mock_get_category):
        mock_get_category.return_value = MockDocument({
            "id": "5678",
            "title": "Electronics",
            "description": "Gadgets and devices"
        })
        category = ProductCategoryService.get_category("5678")
        
        # Ensure consistency: If it's a dict, don't call `.to_dict()`
        if isinstance(category, MockDocument):
            category = category.to_dict()
        
        self.assertEqual(category["id"], "5678")

    @patch.object(ProductCategoryRepository, 'update_category')
    def test_update_category(self, mock_update_category):
        mock_update_category.return_value = 1
        data = {"description": "Updated description"}
        result = ProductCategoryService.update_category("5678", data)
        self.assertEqual(result, 1)

    @patch.object(ProductCategoryRepository, 'delete_category')
    def test_delete_category(self, mock_delete_category):
        mock_delete_category.return_value = 1
        result = ProductCategoryService.delete_category("5678")
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
