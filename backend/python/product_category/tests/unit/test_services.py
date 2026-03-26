import pytest
from product_category.services import ProductCategoryService

from unittest.mock import patch

@patch("product_category.services.ProductCategoryRepository")
def test_create_product_category(mock_repo):

    data = {
        "name": "Fruits",
        "description": "All kinds of fruits"
    }

    mock_repo.create.return_value = data
    
    result = ProductCategoryService.create_product_category(data)
    assert result["name"] == data["name"]
    mock_repo.create.assert_called_once_with(data)

@patch("product_category.services.ProductCategoryRepository")
def test_get_all_product_categories(mock_repo):
    mock_repo.get_all.return_value = [
        {"name": "Fruits", "description": "All kinds of fruits"},
        {"name": "Vegetables", "description": "All kinds of vegetables"}
    ]

    result = ProductCategoryService.get_all_product_categories()
    assert len(result) == 2
    mock_repo.get_all.assert_called_once()

@patch("product_category.services.ProductCategoryRepository")
def test_get_product_category_by_id(mock_repo):
    mock_repo.get_by_id.return_value = {"name": "Fruits", "description": "All kinds of fruits"}

    result = ProductCategoryService.get_product_category_by_id(1)
    assert result["name"] == "Fruits"
    mock_repo.get_by_id.assert_called_once_with(1)

@patch("product_category.services.ProductCategoryRepository")
def test_update_product_category(mock_repo):
    mock_repo.get_by_id.return_value = {"name": "Fruits", "description": "All kinds of fruits"}
    mock_repo.update.return_value = {"name": "Fruits", "description": "Fresh fruits"}

    data = {"description": "Fresh fruits"}
    result = ProductCategoryService.update_product_category(1, data)
    assert result["description"] == "Fresh fruits"
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_called_once_with(1, data)

@patch("product_category.services.ProductCategoryRepository")
def test_update_product_category_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None

    data = {"description": "Fresh fruits"}
    with pytest.raises(ValueError) as excinfo:
        ProductCategoryService.update_product_category(1, data)
    
    assert str(excinfo.value) == "Product Category not found"
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.update.assert_not_called()