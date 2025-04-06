import unittest
from unittest.mock import Mock, patch
from bson import ObjectId
from ..services.CategoryService import CategoryService
from ..models.CategoryModel import ProductCategory
from ..models.ProductModel import Product, ProductHistory

class TestCategoryService(unittest.TestCase):
    CATEGORY_ID=ObjectId()
    PRODUCT_ID=ObjectId()
    
    def setUp(self):
        self.mock_category_repo=Mock()            #create mock repo
        self.category_service=CategoryService()   #create service with mock repo
        self.category_service.repository=self.mock_category_repo
        self.sample_categ_data={'title': 'Test Category','description': 'This is a test category'}     #sample categ. data for testing
        self.sample_categ=Mock(spec=ProductCategory)   #sample categ.
        self.sample_categ.id=ObjectId(self.CATEGORY_ID)
        self.sample_categ.title='Test Category'
        self.sample_categ.description='This is a test category'
        self.sample_prod=Mock(spec=Product)            #sample prod.
        self.sample_prod.id=ObjectId(self.PRODUCT_ID)
        self.sample_prod.name='Test Product'
        self.sample_prod.category=self.sample_categ
    
    def tearDown(self):
        self.mock_category_repo.reset_mock()
        self.mock_category_repo=None
        self.category_service=None
        self.sample_categ=None
        self.sample_prod=None
        self.sample_categ_data=None
    
    def test_create_category(self):
        self.mock_category_repo.create.return_value=self.sample_categ     #configure mock repo to return our sample categ.
        result=self.category_service.create_category(self.sample_categ_data)   #call service method
        self.mock_category_repo.create.assert_called_once_with(self.sample_categ_data)       #assert repo's create method was called with correct data
        self.assertEqual(result,self.sample_categ)      #assert that result is our sample categ.
    
    def test_get_all_categories(self):
        self.mock_category_repo.find_all.return_value=[self.sample_categ]
        result=self.category_service.get_all_categories()
        self.mock_category_repo.find_all.assert_called_once()
        self.assertEqual(result,[self.sample_categ])
    
    def test_get_category_by_id(self):
        self.mock_category_repo.find_by_id.return_value=self.sample_categ
        result=self.category_service.get_category_by_id(self.CATEGORY_ID)
        self.mock_category_repo.find_by_id.assert_called_once_with(self.CATEGORY_ID)
        self.assertEqual(result, self.sample_categ)
    
    def test_get_category_by_id_not_found(self):
        self.mock_category_repo.find_by_id.return_value=None
        result=self.category_service.get_category_by_id('nonexistent_id')
        self.mock_category_repo.find_by_id.assert_called_once_with('nonexistent_id')
        self.assertIsNone(result)
    
    def test_update_category(self):
        updated_data={'title': 'Updated Category','description': 'This is an updated test category'}
        updated_categ=Mock(spec=ProductCategory)
        updated_categ.title='Updated Category'
        updated_categ.description='This is an updated test category'
        self.mock_category_repo.update.return_value=updated_categ
        result=self.category_service.update_category(self.CATEGORY_ID,updated_data)
        self.mock_category_repo.update.assert_called_once_with(self.CATEGORY_ID,updated_data)
        self.assertEqual(result,updated_categ)
    
    def test_update_category_not_found(self):
        updated_data={'title': 'Updated Category','description':'This is an updated category'}
        self.mock_category_repo.update.return_value=None
        result=self.category_service.update_category('nonexistent_id',updated_data)
        self.mock_category_repo.update.assert_called_once_with('nonexistent_id',updated_data)
        self.assertIsNone(result)
    
    def test_delete_category(self):
        self.mock_category_repo.delete.return_value=True
        result=self.category_service.delete_category(self.CATEGORY_ID)
        self.mock_category_repo.delete.assert_called_once_with(self.CATEGORY_ID)
        self.assertTrue(result)
    
    def test_delete_category_not_found(self):
        self.mock_category_repo.delete.return_value=False
        result=self.category_service.delete_category('nonexistent_id')
        self.mock_category_repo.delete.assert_called_once_with('nonexistent_id')
        self.assertFalse(result)
    
    def test_get_products_in_category(self):
        self.mock_category_repo.find_by_id.return_value = self.sample_categ
        mock_product_class=Mock()
        mock_objects=Mock()
        mock_product_class.objects=mock_objects
        mock_filter=Mock(return_value=[self.sample_prod])
        mock_objects.filter=mock_filter
        with patch('product.services.CategoryService.Product', mock_product_class):
            result=self.category_service.get_products_in_category(self.CATEGORY_ID)
            self.mock_category_repo.find_by_id.assert_called_once_with(self.CATEGORY_ID)
            mock_filter.assert_called_once_with(category=self.sample_categ)
            self.assertEqual(result, [self.sample_prod])
    
    def test_get_products_in_category_not_found(self):
        self.mock_category_repo.find_by_id.return_value=None
        result=self.category_service.get_products_in_category('nonexistent_id')
        self.mock_category_repo.find_by_id.assert_called_once_with('nonexistent_id')
        self.assertEqual(result, [])
    
    def test_add_prod_to_category(self):
        mock_category=Mock(spec=ProductCategory)
        mock_category.id=ObjectId(self.CATEGORY_ID)
        mock_product=Mock(spec=Product)
        mock_product.id=ObjectId(self.PRODUCT_ID)
        mock_product.category=None
        with patch('product.services.CategoryService.ProductCategory') as mock_category_class,patch('product.services.CategoryService.Product') as mock_product_class:
            mock_category_class.objects.get.return_value=mock_category
            mock_product_class.objects.get.return_value=mock_product
            result=self.category_service.add_prod_to_category(self.CATEGORY_ID,self.PRODUCT_ID)
            mock_category_class.objects.get.assert_called_once_with(id=self.CATEGORY_ID)
            mock_product_class.objects.get.assert_called_once_with(id=self.PRODUCT_ID)
            self.assertEqual(mock_product.category,mock_category)
            mock_product.save.assert_called_once()
            self.assertTrue(result)
    
    def test_add_prod_to_category_category_not_found(self):
        with patch('product.services.CategoryService.ProductCategory') as mock_category_class:
            mock_category_class.objects.get.side_effect=ProductCategory.DoesNotExist
            result=self.category_service.add_prod_to_category('nonexistent_id',self.PRODUCT_ID)
            self.assertFalse(result)
    
    def test_add_prod_to_category_product_not_found(self):
        mock_category=Mock(spec=ProductCategory)
        mock_category.id=ObjectId(self.CATEGORY_ID)
        with patch('product.services.CategoryService.ProductCategory') as mock_category_class,patch('product.services.CategoryService.Product') as mock_product_class:
            mock_category_class.objects.get.return_value=mock_category
            mock_product_class.objects.get.side_effect=Product.DoesNotExist
            result=self.category_service.add_prod_to_category(self.CATEGORY_ID, 'nonexistent_id')
            self.assertFalse(result)
    
    def test_remove_prod_from_category(self):
        mock_product=Mock(spec=Product)
        mock_product.id=ObjectId(self.PRODUCT_ID)
        mock_product.category=self.sample_categ
        mock_product_history=Mock(spec=ProductHistory)
        with patch('product.services.CategoryService.Product') as mock_product_class,patch('product.services.CategoryService.ProductHistory') as mock_product_history_class:
            mock_product_class.objects.get.return_value=mock_product
            mock_product_history_class.create_version.return_value=mock_product_history
            result = self.category_service.remove_prod_from_category(self.PRODUCT_ID)
            mock_product_class.objects.get.assert_called_once_with(id=self.PRODUCT_ID)
            mock_product_history_class.create_version.assert_called_once_with(mock_product)
            self.assertIsNone(mock_product.category)
            mock_product.save.assert_called_once()
            self.assertTrue(result)
    
    def test_remove_prod_from_category_no_category(self):
        mock_product=Mock(spec=Product)
        mock_product.id=ObjectId(self.PRODUCT_ID)
        mock_product.category=None
        with patch('product.services.CategoryService.Product') as mock_product_class:
            mock_product_class.objects.get.return_value=mock_product
            result=self.category_service.remove_prod_from_category(self.PRODUCT_ID)
            mock_product_class.objects.get.assert_called_once_with(id=self.PRODUCT_ID)
            mock_product.save.assert_not_called()
            self.assertFalse(result)
    
    def test_remove_prod_from_category_product_not_found(self):
        with patch('product.services.CategoryService.Product') as mock_product_class:
            mock_product_class.objects.get.side_effect=Product.DoesNotExist
            result=self.category_service.remove_prod_from_category('nonexistent_id')
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
