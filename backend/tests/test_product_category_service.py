import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
import django
django.setup()

import unittest
from unittest.mock import MagicMock, patch
from product.services.product_category import ProductCategoryService

# from product.services.product_category import ProductCategoryService

class TestProductCategoryService(unittest.TestCase):
    @patch('product.services.product_category.ProductService', autospec=True)
    @patch('product.services.product_category.ProductCategoryRepository', autospec=True)
    def setUp(self, mock_cat_repo_class, mock_product_service_class):
        self.mock_cat_repo = MagicMock()
        mock_cat_repo_class.return_value = self.mock_cat_repo

        self.mock_product_service = MagicMock()
        mock_product_service_class.return_value = self.mock_product_service

        self.product_category_service = ProductCategoryService()


    def test_create_category_success(self):
        data = {'title': 'Test Category', 'description': 'For testing'}
        mock_category = MagicMock()
        self.mock_cat_repo.create_category.return_value = mock_category
        category = self.product_category_service.create_category(data)
        self.mock_cat_repo.create_category.assert_called_once_with(data)
        self.assertEqual(category, mock_category)
    

    def test_get_category_success(self):
        category_id = '123'
        mock_category = MagicMock()
        self.mock_cat_repo.get_category.return_value = mock_category
        category = self.product_category_service.get_category(category_id)
        self.mock_cat_repo.get_category.assert_called_once_with(category_id)
        self.assertEqual(category, mock_category)


    def test_get_category_not_found(self):
        category_id = '123'
        self.mock_cat_repo.get_category.return_value = None
        with self.assertRaises(ValueError):
            self.product_category_service.get_category(category_id)


    def test_update_category_success(self):
        category_id = '123'
        data = {'title':'test', 'description':'for updation test'}

        mock_category = MagicMock()

        self.mock_cat_repo.get_category.return_value = mock_category
        self.mock_cat_repo.update_category.return_value = mock_category

        category = self.product_category_service.update_category(category_id, data)
        
        self.mock_cat_repo.get_category.assert_called_once_with(category_id)
        self.mock_cat_repo.update_category.assert_called_once_with(category_id, data)
        self.assertEqual(category, mock_category)


    def test_update_category_not_found(self):
        category_id ='123'
        data = {'title': 'TEST', 'description': 'for update'}

        self.mock_cat_repo.get_category.return_value = None
        
        with self.assertRaises(ValueError):
            self.product_category_service.update_category(category_id, data)


    def test_delete_category_success(self):
        category_id = '123'
        mock_category = MagicMock()

        self.mock_cat_repo.get_category.return_value = mock_category
        self.mock_cat_repo.delete_category.return_value = mock_category

        category = self.product_category_service.delete_category(category_id)

        self.mock_cat_repo.get_category.assert_called_once_with(category_id)
        self.mock_cat_repo.delete_category.assert_called_once_with(category_id)

        self.assertEqual(category, mock_category)

    
    def test_delete_category_not_found(self):
        category_id = '123'
        self.mock_cat_repo.get_category.return_value = None
        
        with self.assertRaises(ValueError):
            self.product_category_service.delete_category(category_id)

    
    def test_get_all_category(self):
        mock_categories = [MagicMock(), MagicMock()]
        self.mock_cat_repo.get_all_categories.return_value = mock_categories
        
        categories = self.product_category_service.get_all_category()

        self.mock_cat_repo.get_all_categories.assert_called_once()
        self.assertEqual(categories, mock_categories)

    
    def test_list_products_in_category(self):
        category_id = '123'
        mock_products = [MagicMock(), MagicMock()]

        self.mock_cat_repo.list_product_in_category.return_value = mock_products
        products = self.product_category_service.list_products_in_category(category_id)

        self.mock_cat_repo.list_product_in_category.assert_called_once_with(category_id)

        self.assertEqual(products, mock_products)


    def test_add_product_to_category_success(self):
        category_id = '123'
        product_id = '121'

        mock_category = MagicMock()
        mock_product = MagicMock()

        self.mock_cat_repo.get_category.return_value = mock_category
        self.mock_product_service.get_product.return_value = mock_product
        self.mock_product_service.update_product.return_value = mock_product

        product = self.product_category_service.add_product_to_category(category_id, product_id)
        self.mock_cat_repo.get_category.assert_called_once_with(category_id)
        self.mock_product_service.get_product.assert_called_once_with(product_id)
        self.mock_product_service.update_product.assert_called_once_with(product_id, {"category": mock_category})

        self.assertEqual(product, mock_product)


    def test_add_product_to_category_not_found(self):
        category_id = '123'
        product_id = '121'

        mock_category = MagicMock()

        self.mock_cat_repo.get_category.return_value = mock_category
        self.mock_product_service.get_product.return_value = None

        with self.assertRaises(ValueError):
            self.product_category_service.add_product_to_category(category_id, product_id)


    def test_remove_product_from_category_success_when_category_assigned(self):
        category_id = '123'
        product_id = '122'

        mock_category = MagicMock()
        mock_product = MagicMock()

        mock_category.id = category_id
        mock_product.category = mock_category

        self.mock_product_service.get_product.return_value = mock_product
        self.mock_product_service.update_product.return_value = mock_product
        
        product = self.product_category_service.remove_product_from_category(category_id, product_id)

        self.mock_product_service.get_product.assert_called_once_with(product_id)
        self.mock_product_service.update_product.assert_called_once_with(product_id, {"category": None})
        self.assertEqual(product, mock_product)


    def test_remove_product_from_category_success_when_category_not_assigned_or_different_category(self):
        category_id = '123'
        product_id = '122'

        mock_category = MagicMock()
        mock_product = MagicMock()

        mock_category.id = '234'
        mock_product.category = mock_category

        self.mock_product_service.get_product.return_value = mock_product

        product = self.product_category_service.remove_product_from_category(category_id, product_id)

        self.mock_product_service.get_product.assert_called_once_with(product_id)
        self.mock_product_service.update_product.assert_not_called()
        self.assertEqual(product, mock_product)


    def test_remove_product_from_category(self):
        category_id = '123'
        product_id = '122'

        self.mock_product_service.get_product.return_value = None

        with self.assertRaises(ValueError):
            self.product_category_service.remove_product_from_category(category_id, product_id)


if __name__ == '__main__':
    unittest.main(verbosity=2)


        