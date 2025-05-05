import pytest
from unittest.mock import patch, MagicMock
from ...service import ProductService
from ...models import Product
from ..utils import mock_product, mock_category
from mongoengine.errors import ValidationError as MongoValidationError

@pytest.mark.unit
@pytest.mark.service
class TestProductService:
    
    @patch('products.service.ProductRepository')
    def test_get_product_by_slug(self, mock_repo):
        # Arrange
        expected_product = mock_product()
        mock_repo.get_by_slug.return_value = expected_product
        
        # Act
        result = ProductService.get_product_by_slug('mock-product')
        
        # Assert
        assert result == expected_product
        mock_repo.get_by_slug.assert_called_once_with('mock-product')
    
    @patch('products.service.ProductRepository')
    def test_get_product_by_id(self, mock_repo):
        # Arrange
        expected_product = mock_product()
        mock_repo.get_by_id.return_value = expected_product
        
        # Act
        result = ProductService.get_product_by_id('123')
        
        # Assert
        assert result == expected_product
        mock_repo.get_by_id.assert_called_once_with('123')
    
    @patch('products.service.ProductRepository')
    def test_list_products(self, mock_repo):
        # Arrange
        expected_products = [mock_product(), mock_product()]
        mock_repo.list_all.return_value = expected_products
        
        # Act
        result = ProductService.list_products()
        
        # Assert
        assert result == expected_products
        mock_repo.list_all.assert_called_once_with(None)
    
    @patch('products.service.ProductRepository')
    def test_list_products_with_filters(self, mock_repo):
        # Arrange
        expected_products = [mock_product(), mock_product()]
        filters = {'status': 'active'}
        mock_repo.list_all.return_value = expected_products
        
        # Act
        result = ProductService.list_products(filters)
        
        # Assert
        assert result == expected_products
        mock_repo.list_all.assert_called_once_with(filters)
    
    @patch('products.service.ProductRepository')
    def test_create_product_success(self, mock_repo):
        # Arrange
        product_data = {
            'sku': 'ABC-12345',
            'name': 'Test Product',
            'price': 19.99,
            'quantity': 10
        }
        expected_product = mock_product(**product_data)
        mock_repo.create.return_value = expected_product
        
        # Act
        result = ProductService.create_product(product_data)
        
        # Assert
        assert result == expected_product
        mock_repo.create.assert_called_once_with(product_data)
    
    @patch('products.service.ProductRepository')
    def test_create_product_validation_error(self, mock_repo):
        # Arrange
        product_data = {
            'sku': 'invalid',  # Invalid SKU format
            'name': 'Test Product',
            'price': 19.99,
            'quantity': 10
        }
        mock_repo.create.side_effect = MongoValidationError('Invalid SKU format')
        
        # Act & Assert
        with pytest.raises(ValueError, match='Invalid SKU format'):
            ProductService.create_product(product_data)
        
        mock_repo.create.assert_called_once_with(product_data)
    
    @patch('products.service.ProductRepository')
    def test_update_product_success(self, mock_repo):
        # Arrange
        product = mock_product()
        update_data = {'price': 29.99, 'quantity': 5}
        updated_product = mock_product(price=29.99, quantity=5)
        mock_repo.update.return_value = updated_product
        
        # Act
        result = ProductService.update_product(product, update_data)
        
        # Assert
        assert result == updated_product
        mock_repo.update.assert_called_once_with(product, update_data)
    
    @patch('products.service.ProductRepository')
    def test_update_product_validation_error(self, mock_repo):
        # Arrange
        product = mock_product()
        update_data = {'sku': 'invalid'}  # Invalid SKU format
        mock_repo.update.side_effect = MongoValidationError('Invalid SKU format')
        
        # Act & Assert
        with pytest.raises(ValueError, match='Invalid SKU format'):
            ProductService.update_product(product, update_data)
        
        mock_repo.update.assert_called_once_with(product, update_data)
    
    @patch('products.service.ProductRepository')
    def test_delete_product(self, mock_repo):
        # Arrange
        product = mock_product()
        
        # Act
        ProductService.delete_product(product)
        
        # Assert
        mock_repo.delete.assert_called_once_with(product)
    
    @patch('products.service.CategoryRepository')
    def test_filter_products_by_category_found(self, mock_category_repo):
        # Arrange
        category = mock_category()
        mock_category_repo.get_by_slug.return_value = category
        
        # Mock the Product.objects query
        products = [mock_product(), mock_product()]
        
        with patch('products.service.Product') as mock_product_model:
            mock_product_model.objects.return_value = products
            
            # Act
            result = ProductService.filter_products_by_category('test-category')
            
            # Assert
            assert result == products
            mock_category_repo.get_by_slug.assert_called_once_with('test-category')
            mock_product_model.objects.assert_called_once_with(category=category)
    
    @patch('products.service.CategoryRepository')
    def test_filter_products_by_category_not_found(self, mock_category_repo):
        # Arrange
        mock_category_repo.get_by_slug.return_value = None
        
        # Act
        result = ProductService.filter_products_by_category('nonexistent-category')
        
        # Assert
        assert result == []
        mock_category_repo.get_by_slug.assert_called_once_with('nonexistent-category') 