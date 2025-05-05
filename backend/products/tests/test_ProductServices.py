import pytest
from unittest.mock import patch, MagicMock
from products.services import ProductService


@pytest.fixture
def sample_product_data():
    return {
        "product_id": 101,
        "name": "Sample Product",
        "description": "Sample description",
        "category": MagicMock(),  # mocking ProductCategory reference
        "brand": "BrandX"
    }


@patch("products.services.ProductRepository.create_product")
def test_create_product_calls_repository(mock_create_product, sample_product_data):
    mock_created_product = MagicMock()
    mock_create_product.return_value = mock_created_product

    result = ProductService.create_product(sample_product_data)

    mock_create_product.assert_called_once_with(sample_product_data)
    assert result == mock_created_product


@patch("products.services.ProductRepository.get_all_products")
def test_list_products(mock_get_all):
    mock_products = [MagicMock(), MagicMock()]
    mock_get_all.return_value = mock_products

    result = ProductService.list_products()

    mock_get_all.assert_called_once()
    assert result == mock_products


@patch("products.services.ProductRepository.get_product_by_int_id")
def test_retrieve_product(mock_get_by_id):
    mock_product = MagicMock()
    mock_get_by_id.return_value = mock_product

    result = ProductService.retrieve_product(101)

    mock_get_by_id.assert_called_once_with(101)
    assert result == mock_product


@patch("products.services.ProductRepository.update_product")
@patch("products.services.ProductRepository.get_product_by_int_id")
def test_update_product(mock_get_by_id, mock_update):
    mock_product = MagicMock()
    mock_updated_product = MagicMock()
    mock_get_by_id.return_value = mock_product
    mock_update.return_value = mock_updated_product

    update_data = {"name": "Updated Product", "description": "Updated desc"}
    result = ProductService.update_product(101, update_data)

    mock_get_by_id.assert_called_once_with(101)
    mock_update.assert_called_once_with(mock_product, update_data)
    assert result == mock_updated_product


@patch("products.services.ProductRepository.delete_product")
@patch("products.services.ProductRepository.get_product_by_int_id")
def test_delete_product(mock_get_by_id, mock_delete):
    mock_product = MagicMock()
    mock_get_by_id.return_value = mock_product

    result = ProductService.delete_product(101)

    mock_get_by_id.assert_called_once_with(101)
    mock_delete.assert_called_once_with(mock_product)
    assert result == mock_product
