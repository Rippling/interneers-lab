from django.test import TestCase
from unittest.mock import patch

from .services import ProductService

class ProductServiceTest(TestCase):
    
    @patch('products.services.product_repo')
    def test_get_all_products(self,mock_repo):
        
        mock_repo.get_all_products.return_value = [
            {"name": "Fake Mouse", "price": 20.00},
            {"name": "Fake Keyboard", "price": 50.00}
        ]
        service = ProductService()
        result = service.get_all_products()
        
        self.assertEqual(len(result),2)
        self.assertEqual(result[0]['name'],'Fake Mouse')
        
        mock_repo.get_all_products.assert_called_once()
        
        
    @patch('products.services.product_repo')
    def test_get_all_products_with_filters(self,mock_repo):
        
        test_scenarios = [
            {"filters": {"min_price": 50}, "expected_call": {"min_price": 50}, "scenario_name": "Min Price Filter"},
            {"filters": {"brand": "Logitech"}, "expected_call": {"brand": "Logitech"}, "scenario_name": "Brand Filter"},
            {"filters": {"categories": ["ID_1", "ID_2"]}, "expected_call": {"categories": ["ID_1", "ID_2"]}, "scenario_name": "Category Filter"}
        ]
        
        for scenario in test_scenarios:
            
            with self.subTest(msg=scenario['scenario_name']):
                mock_repo.get_all_products.reset_mock()
                
                service = ProductService()
                service.get_all_products(filters=scenario["filters"])
                
                mock_repo.get_all_products.assert_called_once_with(scenario["expected_call"])