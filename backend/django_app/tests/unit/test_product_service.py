import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

import unittest
from unittest.mock import patch, MagicMock
from django_app.services.product_service import ProductService
from django_app.repositories.product_repository import ProductRepository


class TestProductService(unittest.TestCase):

    @patch("django_app.services.product_service.ProductSerializer")
    @patch.object(ProductRepository, "create")
    def test_create_product(self, mock_create, mock_serializer):
        mock_product = MagicMock()
        mock_create.return_value = mock_product
        mock_serializer.return_value.data = {"id": 1, "name": "Laptop"}

        result = ProductService.create_product({"name": "Laptop"})

        self.assertEqual(result, {"id": 1, "name": "Laptop"})
        mock_create.assert_called_once()
        mock_serializer.assert_called_once_with(mock_product)

    @patch("django_app.services.product_service.ProductSerializer")
    @patch.object(ProductRepository, "get_all")
    def test_get_all_products(self, mock_get_all, mock_serializer):
        mock_products = [MagicMock()]
        mock_get_all.return_value = mock_products
        mock_serializer.return_value.data = [{"id": 1, "name": "Laptop"}]

        result = ProductService.get_all_products()

        self.assertEqual(result, [{"id": 1, "name": "Laptop"}])
        mock_get_all.assert_called_once()
        mock_serializer.assert_called_once_with(mock_products, many=True)

    @patch('django_app.services.product_service.ProductSerializer')
    @patch('django_app.repositories.product_repository.ProductRepository.get_by_id')
    def test_get_product_by_id_success(self, mock_get_by_id, mock_serializer):
        mock_product = MagicMock()
        mock_get_by_id.return_value = mock_product

        # Mock serializer return
        mock_serializer.return_value.data = {'id': 1, 'name': 'Mock Product'}

        result = ProductService.get_product_by_id(1)

        self.assertEqual(result, {'id': 1, 'name': 'Mock Product'})


    @patch.object(ProductRepository, "get_by_id")
    def test_get_product_by_id_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None

        result = ProductService.get_product_by_id(99)

        self.assertIsNone(result)
        mock_get_by_id.assert_called_once_with(99)

    @patch("django_app.services.product_service.timezone")
    @patch("django_app.services.product_service.ProductSerializer")
    @patch.object(ProductRepository, "update")
    @patch.object(ProductRepository, "get_by_id")
    def test_update_product_success(self, mock_get_by_id, mock_update, mock_serializer, mock_timezone):
        mock_product = MagicMock()
        mock_get_by_id.return_value = mock_product
        mock_timezone.now.return_value = "mocked-timestamp"
        mock_updated = MagicMock()
        mock_update.return_value = mock_updated
        mock_serializer.return_value.data = {"id": 1, "name": "Updated Product"}

        result = ProductService.update_product({"name": "Updated Product"}, 1)

        self.assertEqual(result, {"id": 1, "name": "Updated Product"})
        mock_get_by_id.assert_called_once_with(1)
        mock_update.assert_called_once()
        mock_serializer.assert_called_once_with(mock_updated)

    @patch.object(ProductRepository, "get_by_id")
    def test_update_product_not_found(self, mock_get_by_id):
        mock_get_by_id.return_value = None
        result = ProductService.update_product({"name": "Updated"}, 999)
        self.assertIsNone(result)

    @patch.object(ProductRepository, "delete")
    def test_delete_product(self, mock_delete):
        ProductService.delete_product("product-id")
        mock_delete.assert_called_once_with("product-id")

    @patch("django_app.services.product_service.ProductSerializer")
    @patch.object(ProductRepository, "get_by_category")
    def test_get_products_by_category(self, mock_get_by_category, mock_serializer):
        mock_products = [MagicMock()]
        mock_get_by_category.return_value = mock_products
        mock_serializer.return_value.data = [{"id": 1, "name": "Laptop"}]

        result = ProductService.get_products_by_category("category-id")

        self.assertEqual(result, [{"id": 1, "name": "Laptop"}])
        mock_get_by_category.assert_called_once_with("category-id")
        mock_serializer.assert_called_once_with(mock_products, many=True)

    @patch("django_app.services.product_service.ProductSerializer")
    @patch.object(ProductRepository, "get_by_name")
    def test_get_product_by_name_found(self, mock_get_by_name, mock_serializer):
        mock_product = MagicMock()
        mock_get_by_name.return_value = mock_product
        mock_serializer.return_value.data = {"id": 1, "name": "Laptop"}

        result = ProductService.get_product_by_name("Laptop")

        self.assertEqual(result, {"id": 1, "name": "Laptop"})
        mock_get_by_name.assert_called_once_with("Laptop")
        mock_serializer.assert_called_once_with(mock_product)

    @patch.object(ProductRepository, "get_by_name")
    def test_get_product_by_name_not_found(self, mock_get_by_name):
        mock_get_by_name.return_value = None

        result = ProductService.get_product_by_name("NonexistentProduct")

        self.assertIsNone(result)
        mock_get_by_name.assert_called_once_with("NonexistentProduct")


if __name__ == "__main__":
    unittest.main(verbosity=2)
