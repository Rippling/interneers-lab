from unittest import TestCase
from unittest.mock import patch, MagicMock
from productAPI.services.product_service import ProductService


class TestProductServiceListProducts(TestCase):

    @patch("productAPI.services.product_service.ProductRepository")
    def test_list_products_no_filters_returns_all(self, MockRepo):
        mock_qs = MagicMock()
        mock_qs.order_by.return_value = mock_qs
        MockRepo.get_all.return_value = mock_qs

        result = ProductService.list_products()

        MockRepo.get_all.assert_called_once()
        self.assertEqual(result, mock_qs)

    @patch("productAPI.services.product_service.ProductCategoryRepository")
    @patch("productAPI.services.product_service.ProductRepository")
    def test_list_products_with_category_filter_resolves_category(self, MockRepo, MockCatRepo):
        mock_category = MagicMock()
        MockCatRepo.get_by_title.return_value = mock_category

        mock_qs = MagicMock()
        mock_qs.order_by.return_value = mock_qs
        MockRepo.get_filtered.return_value = mock_qs

        filters = {"categories": ["Food"]}
        ProductService.list_products(filters=filters)

        MockCatRepo.get_by_title.assert_called_once_with("Food")
        MockRepo.get_filtered.assert_called_once()

    @patch("productAPI.services.product_service.ProductCategoryRepository")
    @patch("productAPI.services.product_service.ProductRepository")
    def test_list_products_skips_unknown_categories(self, MockRepo, MockCatRepo):
        MockCatRepo.get_by_title.return_value = None  

        mock_qs = MagicMock()
        mock_qs.order_by.return_value = mock_qs
        MockRepo.get_filtered.return_value = mock_qs

        ProductService.list_products(filters={"categories": ["NonExistent"]})

        call_args = MockRepo.get_filtered.call_args[0][0]
        self.assertEqual(call_args["categories"], [])

    @patch("productAPI.services.product_service.ProductRepository")
    def test_list_products_sorts_ascending(self, MockRepo):
        mock_qs = MagicMock()
        mock_qs.order_by.return_value = mock_qs
        MockRepo.get_all.return_value = mock_qs

        ProductService.list_products(sortby="asc")

        mock_qs.order_by.assert_called_with("updated_at")

    @patch("productAPI.services.product_service.ProductRepository")
    def test_list_products_sorts_descending_by_default(self, MockRepo):
        mock_qs = MagicMock()
        mock_qs.order_by.return_value = mock_qs
        MockRepo.get_all.return_value = mock_qs

        ProductService.list_products()

        mock_qs.order_by.assert_called_with("-updated_at")


class TestProductServiceCreate(TestCase):

    @patch("productAPI.services.product_service.ProductRepository")
    def test_create_product_delegates_to_repository(self, MockRepo):
        mock_product = MagicMock()
        MockRepo.create.return_value = mock_product

        result = ProductService.create_product({"name": "Veyron", "brand": "Bugatti"})

        MockRepo.create.assert_called_once_with({"name": "Veyron", "brand": "Bugatti"})
        self.assertEqual(result, mock_product)


class TestProductServiceUpdate(TestCase):

    @patch("productAPI.services.product_service.ProductRepository")
    def test_update_product_returns_none_when_not_found(self, MockRepo):
        MockRepo.get_by_id.return_value = None

        result = ProductService.update_product("nonexistent_id", {"name": "Om"})

        self.assertIsNone(result)
        MockRepo.update.assert_not_called()

    @patch("productAPI.services.product_service.ProductRepository")
    def test_update_product_calls_repository_update(self, MockRepo):
        mock_product = MagicMock()
        MockRepo.get_by_id.return_value = mock_product
        MockRepo.update.return_value = mock_product

        result = ProductService.update_product("valid_id", {"name": "Butter"})

        MockRepo.update.assert_called_once_with(mock_product, {"name": "Butter"})
        self.assertEqual(result, mock_product)


class TestProductServiceDelete(TestCase):

    @patch("productAPI.services.product_service.ProductRepository")
    def test_delete_product_returns_none_when_not_found(self, MockRepo):
        MockRepo.get_by_id.return_value = None

        result = ProductService.delete_product("bad_id")

        self.assertIsNone(result)

    @patch("productAPI.services.product_service.ProductRepository")
    def test_delete_product_calls_delete_and_returns_true(self, MockRepo):
        MockRepo.get_by_id.return_value = MagicMock()

        result = ProductService.delete_product("valid_id")

        MockRepo.delete.assert_called_once()
        self.assertTrue(result)


class TestProductServiceAssignCategory(TestCase):

    @patch("productAPI.services.product_service.ProductCategoryRepository")
    @patch("productAPI.services.product_service.ProductRepository")
    def test_assign_category_returns_false_if_product_missing(self, MockRepo, MockCatRepo):
        MockRepo.get_by_id.return_value = None
        MockCatRepo.get_by_id.return_value = MagicMock()

        result = ProductService.assign_category("bad_id", "cat_id")

        self.assertFalse(result)

    @patch("productAPI.services.product_service.ProductCategoryRepository")
    @patch("productAPI.services.product_service.ProductRepository")
    def test_assign_category_returns_false_if_category_missing(self, MockRepo, MockCatRepo):
        MockRepo.get_by_id.return_value = MagicMock()
        MockCatRepo.get_by_id.return_value = None

        result = ProductService.assign_category("prod_id", "bad_cat_id")

        self.assertFalse(result)

    @patch("productAPI.services.product_service.ProductCategoryRepository")
    @patch("productAPI.services.product_service.ProductRepository")
    def test_assign_category_delegates_to_repository(self, MockRepo, MockCatRepo):
        mock_product = MagicMock()
        mock_category = MagicMock()
        MockRepo.get_by_id.return_value = mock_product
        MockCatRepo.get_by_id.return_value = mock_category
        MockRepo.assign_category.return_value = True

        result = ProductService.assign_category("prod_id", "cat_id")

        MockRepo.assign_category.assert_called_once_with(mock_product, mock_category)
        self.assertTrue(result)