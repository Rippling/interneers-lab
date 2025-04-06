import unittest
from unittest.mock import Mock
from decimal import Decimal
from bson import ObjectId
from ..services.ProductService import ProductService
from ..models.ProductModel import Product

class TestProductService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = Mock()       #create a mock repo
        self.prod_service = ProductService()        #create service with mock repo
        self.prod_service.repository = self.mock_repository

        self.categ_id = ObjectId()            #sample valid ObjectIds
        self.prod_id = ObjectId()

        self.sample_prod_data = {                   #sample prod data dictionary
            'name': 'Test Product',
            'description': 'This is test product',
            'price': Decimal('199.99'),
            'brand': 'Test Brand',
            'quantity': 10,
            'category': self.categ_id
        }
        self.sample_prod = Mock(spec=Product)           #sample prod. data
        self.sample_prod.id = self.prod_id
        self.sample_prod.name = 'Test Product'
        self.sample_prod.description = 'This is test product'
        self.sample_prod.price = Decimal('199.99')
        self.sample_prod.brand = 'Test Brand'
        self.sample_prod.quantity = 10
        self.sample_prod.category = self.categ_id
    
    def tearDown(self):         
        self.mock_repository.reset_mock()               #reset all mocks after every test
        self.mock_repository = None
        self.prod_service = None
        self.sample_prod = None
        self.sample_prod_data = None
    
    def test_create_product(self):
        self.mock_repository.create.return_value = self.sample_prod
        result = self.prod_service.create_product(self.sample_prod_data)
        self.mock_repository.create.assert_called_once_with(self.sample_prod_data)
        self.assertEqual(result, self.sample_prod)
    
    def test_get_all_products(self):
        self.mock_repository.get_all.return_value = [self.sample_prod]
        result = self.prod_service.get_all_products()
        self.mock_repository.get_all.assert_called_once()
        self.assertEqual(result, [self.sample_prod])
    
    def test_get_product_by_id(self):
        self.mock_repository.get_by_id.return_value = self.sample_prod
        result = self.prod_service.get_product_by_id(str(self.prod_id))
        self.mock_repository.get_by_id.assert_called_once_with(str(self.prod_id))
        self.assertEqual(result, self.sample_prod)
    
    def test_get_product_by_id_not_found(self):
        self.mock_repository.get_by_id.return_value = None
        invalid_id = str(ObjectId())
        result = self.prod_service.get_product_by_id(invalid_id)
        self.mock_repository.get_by_id.assert_called_once_with(invalid_id)
        self.assertIsNone(result)
    
    def test_update_product(self):
        updated_data = {
            'name': 'Updated Product',
            'price': Decimal('299.99')
        }
        updated_prod = Mock(spec=Product)
        updated_prod.name = 'Updated Product'
        updated_prod.price = Decimal('299.99')
        self.mock_repository.update.return_value = updated_prod
        result = self.prod_service.update_product(str(self.prod_id), updated_data)
        self.mock_repository.update.assert_called_once_with(str(self.prod_id), updated_data)
        self.assertEqual(result, updated_prod)
    
    def test_update_product_not_found(self):
        updated_data = {
            'name': 'Updated Product',
            'price': Decimal('299.99')
        }
        invalid_id=str(ObjectId())
        self.mock_repository.update.return_value = None
        result = self.prod_service.update_product(invalid_id,updated_data)
        self.mock_repository.update.assert_called_once_with(invalid_id,updated_data)
        self.assertIsNone(result)
    
    def test_delete_product(self):
        self.mock_repository.delete.return_value = True
        result = self.prod_service.delete_product(str(self.prod_id))
        self.mock_repository.delete.assert_called_once_with(str(self.prod_id))
        self.assertTrue(result)
    
    def test_delete_product_not_found(self):
        invalid_id=str(ObjectId())
        self.mock_repository.delete.return_value = False
        result = self.prod_service.delete_product(invalid_id)
        self.mock_repository.delete.assert_called_once_with(invalid_id)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
