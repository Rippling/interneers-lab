import unittest
from unittest.mock import Mock
from products.services.product_category_service import ProductCategoryService
from products.repositories.product_category_repository import ProductCategoryDetail


class TestProductCategoryService(unittest.TestCase):
    def setUp(self):
        self.repository = Mock()
        self.service = ProductCategoryService(self.repository)

    def test_get_all_categories(self):
        mock_categories = [
            ProductCategoryDetail(
                title="Electronics", id="1", description="Devices and gadgets"
            ),
            ProductCategoryDetail(
                title="Books", id="2", description="Literature and novels"
            ),
        ]
        self.repository.get_all.return_value = mock_categories

        categories = self.service.get_all_categories()
        
        self.assertEqual(categories, mock_categories)
        self.assertEqual(len(categories), 2)
        self.repository.get_all.assert_called_once()  # Ensure repository method is called once

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

    # Tests for creating a category

    def test_create_category_when_title_exists(self):
        mock_category = ProductCategoryDetail(
            title="Electronics", id="1", description="Devices and gadgets"
        )
        self.repository.get_by_title.return_value = mock_category
        category = ProductCategoryDetail(
            title="Electronics", description="Devices and gadgets"
        )

        self.repository.create.return_value = mock_category
        with self.assertRaises(ValueError) as context:
            self.service.create_category(category)
        self.assertEqual(str(context.exception), "Category title already exists")
        self.repository.get_by_title.assert_called_once_with("Electronics")

    def test_create_category_when_title_is_unique(self):
        category = ProductCategoryDetail(
            title="Toys", id="3", description="Fun and games"
        )
        self.repository.get_by_title.return_value = None
        self.repository.create.return_value = category

        created_category = self.service.create_category(category)
        self.assertEqual(created_category, category)
        self.repository.create.assert_called_once_with(category)

    # Tests for updating a category

    def test_update_category_success_when_title_is_unique(self):
        mock_category = ProductCategoryDetail(
            title="Books", id="2", description="Literature and novels"
        )
        self.repository.get_by_title.return_value = None
        self.repository.update.return_value = mock_category

        category_data = ProductCategoryDetail(
            title="Books", description="Updated description"
        )
        updated_category = self.service.update_category("2", category_data)
        self.assertEqual(updated_category, mock_category)
        self.repository.update.assert_called_once_with("2", category_data)

    def test_update_category_fails_when_title_exists_for_another_category(self):
        existing_category = ProductCategoryDetail(
            title="Toys", id="3", description="Fun and games"
        )
        self.repository.get_by_title.return_value = existing_category
        category_data = ProductCategoryDetail(
            title="Toys", description="Updated description"
        )

        with self.assertRaises(ValueError) as context:
            self.service.update_category("2", category_data)
        self.assertEqual(str(context.exception), "Category title must be unique")
        self.repository.get_by_title.assert_called_once_with("Toys")

    def test_update_category_success_when_title_is_unchanged(self):
        mock_category = ProductCategoryDetail(
            title="Books", id="2", description="Literature and novels"
        )
        self.repository.get_by_title.return_value = mock_category
        category_data = ProductCategoryDetail(
            title="Books", id="2", description="Updated description"
        )
        self.repository.update.return_value = mock_category

        updated_category = self.service.update_category("2", category_data)

        self.assertEqual(updated_category, mock_category)
        self.repository.update.assert_called_once_with("2", category_data)

    # Test for deleting a category

    def test_delete_category_success(self):
        category_id = "123"
        self.repository.delete.return_value = True

        result = self.service.delete_category(category_id)
        self.assertTrue(result)
        self.repository.delete.assert_called_once_with(category_id)

    def test_delete_category_not_found(self):
        category_id = "123"
        self.repository.delete.side_effect = ValueError(
            f"Category with id {category_id} not found"
        )

        with self.assertRaises(ValueError) as context:
            self.service.delete_category(category_id)

        self.assertEqual(
            str(context.exception), f"Category with id {category_id} not found"
        )
        self.repository.delete.assert_called_once_with(category_id)


if __name__ == "__main__":
    unittest.main()
