from django.test import SimpleTestCase
from unittest.mock import MagicMock

from product_csr.services.category_service import CategoryService


class CategoryServiceTests(SimpleTestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.service = CategoryService(self.repo)

    def test_get_all_categories_returns_serialized_categories(self):
        category1 = MagicMock()
        category2 = MagicMock()

        category1.to_dict.return_value = {
            "id": "1",
            "title": "Electronics",
            "description": "Devices",
        }
        category2.to_dict.return_value = {
            "id": "2",
            "title": "Fashion",
            "description": "Clothes",
        }

        self.repo.get_all.return_value = [category1, category2]

        result = self.service.get_all_categories()

        self.repo.get_all.assert_called_once()
        self.assertEqual(result, [
            {"id": "1", "title": "Electronics", "description": "Devices"},
            {"id": "2", "title": "Fashion", "description": "Clothes"},
        ])

    def test_get_category_returns_serialized_category(self):
        category = MagicMock()
        category.to_dict.return_value = {
            "id": "1",
            "title": "Electronics",
            "description": "Devices",
        }

        self.repo.get_by_id.return_value = category

        result = self.service.get_category("cat1")

        self.repo.get_by_id.assert_called_once_with("cat1")
        self.assertEqual(result, {
            "id": "1",
            "title": "Electronics",
            "description": "Devices",
        })

    def test_get_category_raises_when_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "category not found"):
            self.service.get_category("cat1")

    def test_create_category_raises_when_title_missing(self):
        with self.assertRaisesMessage(ValueError, "Title is required"):
            self.service.create_category({"description": "Devices"})

    def test_create_category_success(self):
        data = {
            "title": "Electronics",
            "description": "Devices",
        }
        category = MagicMock()
        category.to_dict.return_value = {
            "id": "1",
            "title": "Electronics",
            "description": "Devices",
        }

        self.repo.create.return_value = category

        result = self.service.create_category(data)

        self.repo.create.assert_called_once_with(data)
        self.assertEqual(result, {
            "id": "1",
            "title": "Electronics",
            "description": "Devices",
        })

    def test_update_category_raises_when_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "category not found"):
            self.service.update_category("cat1", {"title": "Updated"})

    def test_update_category_success(self):
        category = MagicMock()
        updated_category = MagicMock()
        data = {
            "title": "Updated Electronics",
            "description": "Updated description",
        }

        updated_category.to_dict.return_value = {
            "id": "1",
            "title": "Updated Electronics",
            "description": "Updated description",
        }

        self.repo.get_by_id.return_value = category
        self.repo.update.return_value = updated_category

        result = self.service.update_category("cat1", data)

        self.repo.get_by_id.assert_called_once_with("cat1")
        self.repo.update.assert_called_once_with(category, data)
        self.assertEqual(result, {
            "id": "1",
            "title": "Updated Electronics",
            "description": "Updated description",
        })

    def test_delete_category_raises_when_not_found(self):
        self.repo.get_by_id.return_value = None

        with self.assertRaisesMessage(ValueError, "category not found"):
            self.service.delete_category("cat1")

    def test_delete_category_success(self):
        category = MagicMock()
        self.repo.get_by_id.return_value = category

        result = self.service.delete_category("cat1")

        self.repo.delete.assert_called_once_with(category)
        self.assertEqual(result, {"message": "category deleted successfully"})

    def test_create_category_if_not_exists_returns_existing(self):
        existing = MagicMock()
        self.repo.get_by_title.return_value = existing

        result = self.service.create_category_if_not_exists("Electronics")

        self.repo.get_by_title.assert_called_once_with("Electronics")
        self.repo.create.assert_not_called()
        self.assertIs(result, existing)

    def test_create_category_if_not_exists_creates_new_category(self):
        created = MagicMock()
        self.repo.get_by_title.return_value = None
        self.repo.create.return_value = created

        result = self.service.create_category_if_not_exists("Electronics")

        self.repo.get_by_title.assert_called_once_with("Electronics")
        self.repo.create.assert_called_once_with({
            "title": "Electronics",
            "description": "",
        })
        self.assertIs(result, created)
