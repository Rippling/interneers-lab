import pytest
from unittest.mock import patch
from ...service import CategoryService
from ..utils import mock_category

@pytest.mark.unit
@pytest.mark.service
class TestCategoryService:
    
    @patch('products.service.CategoryRepository')
    def test_get_category_by_slug(self, mock_repo):
        # Arrange
        expected_category = mock_category()
        mock_repo.get_by_slug.return_value = expected_category
        
        # Act
        result = CategoryService.get_category_by_slug('mock-category')
        
        # Assert
        assert result == expected_category
        mock_repo.get_by_slug.assert_called_once_with('mock-category')
    
    @patch('products.service.CategoryRepository')
    def test_get_category_by_id(self, mock_repo):
        # Arrange
        expected_category = mock_category()
        mock_repo.get_by_id.return_value = expected_category
        
        # Act
        result = CategoryService.get_category_by_id('123')
        
        # Assert
        assert result == expected_category
        mock_repo.get_by_id.assert_called_once_with('123')
    
    @patch('products.service.CategoryRepository')
    def test_list_categories(self, mock_repo):
        # Arrange
        expected_categories = [mock_category(), mock_category()]
        mock_repo.list_all.return_value = expected_categories
        
        # Act
        result = CategoryService.list_categories()
        
        # Assert
        assert result == expected_categories
        mock_repo.list_all.assert_called_once()
    
    @patch('products.service.CategoryRepository')
    def test_create_category(self, mock_repo):
        # Arrange
        category_data = {
            'name': 'Test Category',
            'description': 'Test category description'
        }
        expected_category = mock_category(**category_data)
        mock_repo.create.return_value = expected_category
        
        # Act
        result = CategoryService.create_category(category_data)
        
        # Assert
        assert result == expected_category
        mock_repo.create.assert_called_once_with(category_data)
    
    @patch('products.service.CategoryRepository')
    def test_delete_category(self, mock_repo):
        # Arrange
        category = mock_category()
        
        # Act
        CategoryService.delete_category(category)
        
        # Assert
        mock_repo.delete.assert_called_once_with(category) 