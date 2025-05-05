import pytest
from unittest.mock import patch
from ...service import ProductService
from ..utils import mock_product, mock_category

@pytest.mark.unit
@pytest.mark.service
@pytest.mark.parametrize("status, expected_call", [
    ('active', 'active'),
    ('inactive', 'inactive'),
    ('out_of_stock', 'out_of_stock'),
    ('discontinued', 'discontinued'),
])
def test_filter_products_by_status_parameterized(status, expected_call):
    """Test filtering products by status with parameterized test cases"""
    with patch('products.service.Product') as mock_product_model:
        # Act
        ProductService.filter_products_by_status(status)
        
        # Assert
        mock_product_model.objects.assert_called_once_with(status=expected_call)

@pytest.mark.unit
@pytest.mark.service
@pytest.mark.parametrize("price, discount_price, should_raise", [
    (100, 80, False),    # Valid: discount < price
    (100, 100, True),    # Invalid: discount == price
    (100, 120, True),    # Invalid: discount > price
    (100, None, False),  # Valid: no discount
])
def test_validate_discount_price_parameterized(price, discount_price, should_raise):
    """Test validating that discount price is less than regular price"""
    # Arrange
    from ...serializers import ProductSerializer
    
    # Create data with the parameterized values
    data = {
        'price': price,
    }
    if discount_price is not None:
        data['discount_price'] = discount_price
    
    serializer = ProductSerializer()
    
    # Act & Assert
    if should_raise:
        with pytest.raises(Exception):
            serializer.validate(data)
    else:
        # Shouldn't raise an exception
        result = serializer.validate(data)
        assert result == data

@pytest.mark.unit
@pytest.mark.service
@pytest.mark.parametrize("dimensions, should_raise", [
    ('10x20x30', False),      # Valid format
    ('10.5x20.5x30.5', False), # Valid with decimals
    ('10x20', True),          # Invalid: missing one dimension
    ('axbxc', True),          # Invalid: not numbers
    ('10,20,30', True),       # Invalid: wrong separator
])
def test_validate_dimensions_parameterized(dimensions, should_raise):
    """Test validating dimensions format with parameterized test cases"""
    # Arrange
    from ...serializers import ProductSerializer
    
    # Create data with the parameterized values
    data = {
        'price': 100,
        'dimensions': dimensions
    }
    
    serializer = ProductSerializer()
    
    # Act & Assert
    if should_raise:
        with pytest.raises(Exception):
            serializer.validate(data)
    else:
        # Shouldn't raise an exception
        result = serializer.validate(data)
        assert result == data 