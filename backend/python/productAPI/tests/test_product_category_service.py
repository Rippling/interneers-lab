from unittest import TestCase
from unittest.mock import patch, MagicMock
from productAPI.services.product_category_service import ProductCategoryService


class TestProductCategoryServiceGet(TestCase):

    @patch("productAPI.services.product_category_service.ProductCategoryRepository")
    def test_get_categories_returns_all_without_pagination(self, MockRepo):
        mock_qs = MagicMock()
        MockRepo.get_all.return_value = mock_qs

        result = ProductCategoryService.get_categories()

        MockRepo.get_all.assert_called_once()
        self.assertEqual(result, mock_qs)

    @patch("productAPI.services.product_category_service.ProductCategoryRepository")
    def test_get_categories_paginates_when_page_provided(self, MockRepo):
        MockRepo.get_all.return_value = [MagicMock() for _ in range(10)]

        result = ProductCategoryService.get_categories(page_number=1)

        self.assertIsNotNone(result)


class TestProductCategoryServiceCreate(TestCase):

    @patch("productAPI.services.product_category_service.ProductCategoryRepository")
    def test_create_category_delegates_to_repository(self, MockRepo):
        mock_cat = MagicMock()
        MockRepo.create.return_value = mock_cat

        result = ProductCategoryService.create_category({"title": "Food"})

        MockRepo.create.assert_called_once_with({"title": "Food"})
        self.assertEqual(result, mock_cat)


class TestProductCategoryServiceUpdate(TestCase):

    @patch("productAPI.services.product_category_service.ProductCategoryRepository")
    def test_update_returns_none_when_not_found(self, MockRepo):
        MockRepo.get_by_id.return_value = None

        result = ProductCategoryService.update_category("bad_id", {"title": "X"})

        self.assertIsNone(result)
        MockRepo.update.assert_not_called()

    @patch("productAPI.services.product_category_service.ProductCategoryRepository")
    def test_update_calls_repository_update(self, MockRepo):
        mock_cat = MagicMock()
        MockRepo.get_by_id.return_value = mock_cat
        MockRepo.update.return_value = mock_cat

        result = ProductCategoryService.update_category("valid_id", {"title": "Electronics"})

        MockRepo.update.assert_called_once_with(mock_cat, {"title": "Electronics"})
        self.assertEqual(result, mock_cat)


class TestProductCategoryServiceDelete(TestCase):

    @patch("productAPI.services.product_category_service.ProductCategoryRepository")
    def test_delete_returns_none_when_not_found(self, MockRepo):
        MockRepo.get_by_id.return_value = None

        result = ProductCategoryService.delete_category("bad_id")

        self.assertIsNone(result)

    @patch("productAPI.services.product_category_service.ProductCategoryRepository")
    def test_delete_calls_repository_and_returns_true(self, MockRepo):
        MockRepo.get_by_id.return_value = MagicMock()

        result = ProductCategoryService.delete_category("valid_id")

        MockRepo.delete.assert_called_once()
        self.assertTrue(result)