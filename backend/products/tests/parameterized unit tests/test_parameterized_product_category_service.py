import unittest
from unittest.mock import Mock
from parameterized import parameterized
from products.services.product_category_service import ProductCategoryService
from products.repositories.product_category_repository import ProductCategoryDetail


class TestProductCategoryService(unittest.TestCase):
    def setUp(self):
        self.repository = Mock()
        self.service = ProductCategoryService(self.repository)

    @parameterized.expand([
        ("multiple_categories", [
            ProductCategoryDetail(title="Electronics", id="1", description="Devices"),
            ProductCategoryDetail(title="Books", id="2", description="Literature")
        ], 2),
        ("empty_list", [], 0),
        ("single_category", [
            ProductCategoryDetail(title="Clothing", id="3", description="Apparel")
        ], 1)
    ])
    def test_get_all_categories(self, _, mock_data, expected_count):
        self.repository.get_all.return_value = mock_data
        result = self.service.get_all_categories()
        self.assertEqual(len(result), expected_count)
        self.repository.get_all.assert_called_once()

    @parameterized.expand([
        ("existing_id", "1", ProductCategoryDetail(
            title="Electronics", id="1", description="Devices")),
        ("non_existing_id", "999", None)
    ])
    def test_category_by_id(self, _, category_id, expected_result):
        self.repository.get_by_id.return_value = expected_result
        result = self.service.get_category_by_id(category_id)
        self.assertEqual(result, expected_result)
        self.repository.get_by_id.assert_called_once_with(category_id)

    @parameterized.expand([
        ("existing_title", "Books", ProductCategoryDetail(
            title="Books", id="2", description="Literature")),
        ("non_existing_title", "NonExisting", None)
    ])
    def test_category_by_title(self, _, title, expected_result):
        self.repository.get_by_title.return_value = expected_result
        result = self.service.get_category_by_title(title)
        self.assertEqual(result, expected_result)
        self.repository.get_by_title.assert_called_once_with(title)

    @parameterized.expand([
        ("title_exists", "Electronics", True, "Category title already exists"),
        ("title_unique", "NewCategory", False, None),
    ])
    def test_create_category(self, _, title, title_exists, expected_error):
        category_data = ProductCategoryDetail(
            title=title, description="Test description"
        )
        
        self.repository.get_by_title.return_value = (
            ProductCategoryDetail(title=title, id="1") if title_exists else None
        )
        
        if expected_error:
            with self.assertRaises(ValueError) as cm:
                self.service.create_category(category_data)
            self.assertEqual(str(cm.exception), expected_error)
            self.repository.create.assert_not_called()
        else:
            self.repository.create.return_value = category_data
            result = self.service.create_category(category_data)
            self.assertEqual(result, category_data)
            self.repository.create.assert_called_once_with(category_data)
        
        self.repository.get_by_title.assert_called_once_with(title)

    @parameterized.expand([
        ("update_with_unique_title", "2", "NewTitle", None, None),
        ("title_exists_other_category", "2", "ExistingTitle", 
         ProductCategoryDetail(id="3", title="ExistingTitle"), 
         "Category title must be unique"),
        ("title_unchanged", "2", "OriginalTitle", 
         ProductCategoryDetail(id="2", title="OriginalTitle"), None),
    ])
    def test_update_category(self, _, category_id, new_title, 
                            existing_category, error_msg):
        update_data = ProductCategoryDetail(
            title=new_title, 
            description="Updated description"
        )
        
        self.repository.get_by_title.return_value = existing_category
        self.repository.update.return_value = update_data

        if error_msg:
            with self.assertRaises(ValueError) as cm:
                self.service.update_category(category_id, update_data)
            self.assertEqual(str(cm.exception), error_msg)
            self.repository.update.assert_not_called()
        else:
            result = self.service.update_category(category_id, update_data)
            self.assertEqual(result, update_data)
            self.repository.update.assert_called_once_with(category_id, update_data)
        
        self.repository.get_by_title.assert_called_once_with(new_title)

    @parameterized.expand([
        ("delete_success", "123", True),
        ("delete_not_found", "456", False),
    ])
    def test_delete_category(self, _, category_id, expected_result):
        if isinstance(expected_result, bool):
            self.repository.delete.return_value = expected_result
            result = self.service.delete_category(category_id)
            self.assertEqual(result, expected_result)
        else:
            self.repository.delete.side_effect = ValueError(expected_result)
            with self.assertRaises(ValueError) as cm:
                self.service.delete_category(category_id)
            self.assertEqual(str(cm.exception), expected_result)
        
        self.repository.delete.assert_called_once_with(category_id)


if __name__ == "__main__":
    unittest.main()