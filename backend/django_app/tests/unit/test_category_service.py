import os
import django
import unittest
from unittest.mock import patch, MagicMock

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

from django_app.services.category_service import CategoryService


class TestCategoryService(unittest.TestCase):

    @patch("django_app.services.category_service.CategorySerializer")
    @patch("django_app.repositories.category_repository.CategoryRepository.create")
    def test_create_category(self, mock_create, mock_serializer):
        mock_category = MagicMock()
        mock_category.id = "1"
        mock_category.title = "Electronics"
        mock_category.description = "Devices and gadgets"
        mock_category.created_at = "2024-01-01T00:00:00Z"
        mock_category.updated_at = "2024-01-01T00:00:00Z"

        mock_create.return_value = mock_category
        mock_serializer.return_value.data = {
            "id": "1",
            "title": "Electronics",
            "description": "Devices and gadgets",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }

        result = CategoryService.create_category({
            "title": "Electronics",
            "description": "Devices and gadgets"
        })

        self.assertEqual(result, {
            "id": "1",
            "title": "Electronics",
            "description": "Devices and gadgets",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        })

        mock_create.assert_called_once()
        mock_serializer.assert_called_once_with(mock_category)


    @patch("django_app.services.category_service.CategorySerializer")
    @patch("django_app.repositories.category_repository.CategoryRepository.get_all")
    def test_get_all_categories(self, mock_get_all, mock_serializer):
        mock_category = MagicMock()
        mock_category.id = "1"
        mock_category.title = "Electronics"

        mock_get_all.return_value = [mock_category]
        mock_serializer.return_value.data = [
            {"id": "1", "title": "Electronics"}
        ]

        result = CategoryService.get_all_categories()

        self.assertEqual(result, [{"id": "1", "title": "Electronics"}])

        mock_get_all.assert_called_once()
        mock_serializer.assert_called_once_with([mock_category], many=True)


    @patch("django_app.services.category_service.CategorySerializer")
    @patch("django_app.repositories.category_repository.CategoryRepository.get_by_id")
    def test_get_category_by_id_found(self, mock_get_by_id, mock_serializer):
        mock_category = MagicMock()
        mock_category.id = "1"
        mock_category.title = "Electronics"

        mock_get_by_id.return_value = mock_category
        mock_serializer.return_value.data = {"id": "1", "title": "Electronics"}

        result = CategoryService.get_category_by_id("1")

        self.assertEqual(result, {"id": "1", "title": "Electronics"})

        mock_get_by_id.assert_called_once_with("1")
        mock_serializer.assert_called_once_with(mock_category)


    @patch("django_app.repositories.category_repository.CategoryRepository.get_by_id")
    def test_get_category_by_id_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        result = CategoryService.get_category_by_id("nonexistent_id")
        self.assertIsNone(result)

    @patch("django_app.services.category_service.CategorySerializer")
    @patch("django_app.repositories.category_repository.CategoryRepository.update")
    @patch("django_app.repositories.category_repository.CategoryRepository.get_by_id")
    def test_update_category_success(self, mock_get_by_id, mock_update, mock_serializer):
        mock_category = MagicMock()
        mock_category.id = "1"
        mock_get_by_id.return_value = mock_category

        mock_updated_category = MagicMock()
        mock_updated_category.id = "1"
        mock_updated_category.title = "Updated"
        mock_update.return_value = mock_updated_category

        mock_serializer.return_value.data = {"id": "1", "title": "Updated"}

        update_data = {"title": "Updated"}

        result = CategoryService.update_category(update_data, "1")

        self.assertEqual(result, {"id": "1", "title": "Updated"})

        mock_get_by_id.assert_called_once_with("1")
        mock_update.assert_called_once_with(mock_category, update_data)
        mock_serializer.assert_called_once_with(mock_updated_category)


    @patch("django_app.repositories.category_repository.CategoryRepository.get_by_id")
    def test_update_category_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        result = CategoryService.update_category({"title": "New"}, "invalid")
        self.assertIsNone(result)

    @patch("django_app.repositories.category_repository.CategoryRepository.delete")
    def test_delete_category(self, mock_delete):
        CategoryService.delete_category("1")
        mock_delete.assert_called_once_with("1")

    @patch("django_app.services.category_service.CategorySerializer")
    @patch("django_app.repositories.category_repository.CategoryRepository.get_by_title")
    def test_get_category_by_title_found(self, mock_get_by_title, mock_serializer):
        mock_category = MagicMock()
        mock_category.title = "Electronics"

        mock_get_by_title.return_value = mock_category
        mock_serializer.return_value.data = {"title": "Electronics"}

        result = CategoryService.get_category_by_title("Electronics")

        self.assertEqual(result, {"title": "Electronics"})
        mock_get_by_title.assert_called_once_with("Electronics")
        mock_serializer.assert_called_once_with(mock_category)

    @patch("django_app.repositories.category_repository.CategoryRepository.get_by_title")
    def test_get_category_by_title_not_found(self, mock_get_by_title):
        mock_get_by_title.return_value = None
        result = CategoryService.get_category_by_title("Nonexistent")
        self.assertIsNone(result)
        mock_get_by_title.assert_called_once_with("Nonexistent")



if __name__ == "__main__":
    unittest.main(verbosity=2)
