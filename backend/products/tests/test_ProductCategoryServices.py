import pytest
from unittest.mock import patch, MagicMock
from products.services import ProductCategoryService


@pytest.fixture
def sample_category_data():
    return {
        "category_id": 1,
        "name": "Electronics",
        "description": "Electronic products"
    }


@patch("products.services.ProductCategoryRepository.create_category")
def test_create_category(mock_create_category, sample_category_data):
    mock_category = MagicMock()
    mock_create_category.return_value = mock_category

    result = ProductCategoryService.create_category(sample_category_data)

    mock_create_category.assert_called_once_with(sample_category_data)
    assert result == mock_category


@patch("products.services.ProductCategoryRepository.get_all_categories")
def test_list_categories(mock_get_all):
    mock_categories = [MagicMock(), MagicMock()]
    mock_get_all.return_value = mock_categories

    result = ProductCategoryService.list_categories()

    mock_get_all.assert_called_once()
    assert result == mock_categories


@patch("products.services.ProductCategoryRepository.get_category_by_id")
def test_retrieve_category(mock_get_by_id):
    mock_category = MagicMock()
    mock_get_by_id.return_value = mock_category

    result = ProductCategoryService.retrieve_category(1)

    mock_get_by_id.assert_called_once_with(1)
    assert result == mock_category


@patch("products.services.ProductCategoryRepository.update_category")
@patch("products.services.ProductCategoryRepository.get_category_by_id")
def test_update_category(mock_get_by_id, mock_update):
    mock_category = MagicMock()
    updated_category = MagicMock()
    mock_get_by_id.return_value = mock_category
    mock_update.return_value = updated_category

    update_data = {"name": "Updated Electronics"}
    result = ProductCategoryService.update_category(1, update_data)

    mock_get_by_id.assert_called_once_with(1)
    mock_update.assert_called_once_with(mock_category, update_data)
    assert result == updated_category


@patch("products.services.ProductCategoryRepository.delete_category")
@patch("products.services.ProductCategoryRepository.get_category_by_id")
def test_delete_category(mock_get_by_id, mock_delete):
    mock_category = MagicMock()
    mock_get_by_id.return_value = mock_category

    result = ProductCategoryService.delete_category(1)

    mock_get_by_id.assert_called_once_with(1)
    mock_delete.assert_called_once_with(mock_category)
    assert result == mock_category
