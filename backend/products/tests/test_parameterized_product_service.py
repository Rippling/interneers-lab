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
            ProductCategoryDetail(title="Electronics", id="1", description="Devices and gadgets"),
            ProductCategoryDetail(title="Books", id="2", description="Literature and novels")
        ]),
        ("empty_list", []),
        ("single_category", [
            ProductCategoryDetail(title="Clothing", id="3", description="Apparel")
        ])
    ])
    
    def test_get_all_categories(self, name, mock_data):
        self.repository.get_all.return_value = mock_data

        result = self.service.get_all_categories()

        self.assertEqual(result, mock_data)
        self.assertEqual(len(result), len(mock_data))
        self.repository.get_all.assert_called_once()

    def test_category_by_id(self):
        mock_category = ProductCategoryDetail(
            title="Electronics", id="1", description="Devices and gadgets"
        )
        self.repository.get_by_id.return_value = mock_category

        category = self.service.get_category_by_id("1")
        self.assertEqual(category, mock_category)
        self.repository.get_by_id.assert_called_once_with("1")

    def test_category_by_title(self):
        mock_category = ProductCategoryDetail(
            title="Books", id="2", description="Literature and novels"
        )
        self.repository.get_by_title.return_value = mock_category

        category = self.service.get_category_by_title("Books")
        self.assertEqual(category, mock_category)
        self.repository.get_by_title.assert_called_once_with("Books")

    @parameterized.expand([
        ("title_exists", "Electronics", "Devices and gadgets", True, "Category title already exists"),
        ("title_unique", "Toys", "Fun and games", False, None),
    ])
    def test_create_category(self, _, title, description, title_exists, expected_error):
        category_data = ProductCategoryDetail(title=title, description=description)
        if title_exists:
            self.repository.get_by_title.return_value = ProductCategoryDetail(
                title=title, id="1", description=description
            )
        else:
            self.repository.get_by_title.return_value = None

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
        ("unique_title", "2", "NewTitle", None, None),
        ("title_exists_other_id", "2", "Toys", ProductCategoryDetail(id="3", title="Toys"), "Category title must be unique"),
        ("title_unchanged", "2", "Books", ProductCategoryDetail(id="2", title="Books"), None),
    ])
    def test_update_category(self, _, category_id, new_title, existing_category, expected_error):
        update_data = ProductCategoryDetail(title=new_title, description="Updated")
        self.repository.get_by_title.return_value = existing_category

        if expected_error:
            with self.assertRaises(ValueError) as cm:
                self.service.update_category(category_id, update_data)
            self.assertEqual(str(cm.exception), expected_error)
            self.repository.update.assert_not_called()
        else:
            self.repository.update.return_value = update_data
            result = self.service.update_category(category_id, update_data)
            self.assertEqual(result, update_data)
            self.repository.update.assert_called_once_with(category_id, update_data)
        self.repository.get_by_title.assert_called_once_with(new_title)

    @parameterized.expand([
        ("success", "123", True, None),
        ("not_found", "456", None, "Category with id 456 not found"),
    ])
    def test_delete_category(self, _, category_id, repo_result, error_msg):
        if error_msg:
            self.repository.delete.side_effect = ValueError(error_msg)
            with self.assertRaises(ValueError) as cm:
                self.service.delete_category(category_id)
            self.assertEqual(str(cm.exception), error_msg)
        else:
            self.repository.delete.return_value = repo_result
            result = self.service.delete_category(category_id)
            self.assertEqual(result, repo_result)
        self.repository.delete.assert_called_once_with(category_id)


if __name__ == "__main__":
    unittest.main()