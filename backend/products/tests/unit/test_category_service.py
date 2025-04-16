import pytest
from unittest.mock import patch, MagicMock
from django.http import Http404
from products.services.CategoryService import CategoryService
from products.repositories.Category import CategoryRepository


@pytest.mark.parametrize(
    "title, description",
    [
        ("Electronics", "Category for electronic items"),
        ("Books", None),
    ],
)

@patch("products.repositories.Category.CategoryRepository.create")
def test_create_category(mock_create, title, description):
    mock_create.return_value = {"title": title, "description": description}

    result = CategoryService.create_category(title, description)

    mock_create.assert_called_once_with(title, description)
    assert result == {"title": title, "description": description}


@patch("products.repositories.Category.CategoryRepository.get_category_by_title")
@patch("products.repositories.Category.CategoryRepository.get_products_by_category")
def test_get_products_by_category_title_found(mock_get_products, mock_get_category):
    mock_category = MagicMock()
    mock_get_category.return_value = mock_category
    mock_get_products.return_value = [{"name": "Laptop"}, {"name": "Smartphone"}]

    products, error = CategoryService.get_products_by_category_title("Electronics")

    assert products == [{"name": "Laptop"}, {"name": "Smartphone"}]
    assert error is None
    mock_get_category.assert_called_once_with("Electronics")
    mock_get_products.assert_called_once_with(mock_category)


@patch("products.repositories.Category.CategoryRepository.get_category_by_title")
def test_get_products_by_category_title_not_found(mock_get_category):
    mock_get_category.return_value = None

    products, error = CategoryService.get_products_by_category_title("Nonexistent")

    assert products is None
    assert error == "Category not found"
    mock_get_category.assert_called_once_with("Nonexistent")


@patch("products.repositories.Category.CategoryRepository.getCategoryById")
def test_get_category_by_id_found(mock_get_category):
    mock_category = MagicMock()
    mock_get_category.return_value = mock_category

    result = CategoryService.getCategoryById("123")

    assert result == mock_category
    mock_get_category.assert_called_once_with("123")


@patch("products.repositories.Category.CategoryRepository.getCategoryById")
def test_get_category_by_id_not_found(mock_get_category):
    mock_get_category.return_value = None

    with pytest.raises(Http404, match="Category not found"):
        CategoryService.getCategoryById("invalid_id")

    mock_get_category.assert_called_once_with("invalid_id")


@patch("products.repositories.Category.CategoryRepository.get_all")
def test_get_all_categories(mock_get_all):
    mock_get_all.return_value = [
        {"title": "Electronics"},
        {"title": "Books"},
    ]

    result = CategoryService.get_all_categories()

    assert isinstance(result, list)
    assert len(result) == 2
    mock_get_all.assert_called_once()


@patch("products.repositories.Category.CategoryRepository.update")
def test_update_category(mock_update):
    mock_update.return_value = True

    result = CategoryService.update_category("Old Title", "New Title", "New Description")

    assert result is True
    mock_update.assert_called_once_with("Old Title", "New Title", "New Description")


@patch("products.repositories.Category.CategoryRepository.delete")
def test_delete_category(mock_delete):
    mock_delete.return_value = True

    result = CategoryService.delete_category("Electronics")

    assert result is True
    mock_delete.assert_called_once_with("Electronics")
