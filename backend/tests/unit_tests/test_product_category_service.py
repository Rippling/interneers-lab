import pytest
from product.services.product_category_service import ProductCategoryService

@pytest.fixture
def mock_category_repository(mocker):
    return mocker.MagicMock()

@pytest.fixture
def category_service(mock_category_repository, mocker):
    mocker.patch(
        "product.services.product_category_service.ProductCategoryRepository",
        return_value=mock_category_repository
    )
    return ProductCategoryService()

def test_create_category_success(category_service, mock_category_repository):
    data = {"title": "Books", "description": "All kinds of books"}
    mock_category_repository.create_category.return_value = data

    result = category_service.create_category(data)

    mock_category_repository.create_category.assert_called_once_with(data)
    assert result == data

def test_create_category_duplicate(category_service, mock_category_repository):
    from mongoengine.errors import NotUniqueError
    mock_category_repository.create_category.side_effect = NotUniqueError()

    with pytest.raises(ValueError, match="Category with this name already exists."):
        category_service.create_category({"title": "Duplicate"})

def test_get_all_categories_success(category_service, mock_category_repository):
    mock_categories = [{"title": "Books"}, {"title": "Electronics"}]
    mock_category_repository.get_all_categories.return_value = mock_categories

    result = category_service.get_all_categories()

    mock_category_repository.get_all_categories.assert_called_once()
    assert result == mock_categories

def test_get_all_categories_empty(category_service, mock_category_repository):
    mock_category_repository.get_all_categories.return_value = []

    result = category_service.get_all_categories()

    mock_category_repository.get_all_categories.assert_called_once()
    assert result == []

def test_get_category_by_id_success(category_service, mock_category_repository):
    category_id = "507f1f77bcf86cd799439011"
    mock_category = {"id": category_id, "title": "Books"}
    mock_category_repository.get_category_by_id.return_value = mock_category

    result = category_service.get_category_by_id(category_id)

    mock_category_repository.get_category_by_id.assert_called_once_with(category_id)
    assert result == mock_category

def test_get_category_by_id_invalid(category_service, mock_category_repository):
    invalid_id = "invalid_id"

    result = category_service.get_category_by_id(invalid_id)

    mock_category_repository.get_category_by_id.assert_not_called()
    assert result is None

def test_get_category_by_id_not_found(category_service, mock_category_repository):
    category_id = "507f1f77bcf86cd799439012"
    mock_category_repository.get_category_by_id.return_value = None

    result = category_service.get_category_by_id(category_id)

    mock_category_repository.get_category_by_id.assert_called_once_with(category_id)
    assert result is None

def test_update_category_success(category_service, mock_category_repository):
    category_id = "507f1f77bcf86cd799439011"
    updated_data = {"title": "Updated Title"}
    existing_category = {"id": category_id, "title": "Books"}
    updated_category = {"id": category_id, "title": "Updated Title"}

    mock_category_repository.get_category_by_id.return_value = existing_category
    mock_category_repository.update_category.return_value = updated_category

    result = category_service.update_category(category_id, updated_data)

    mock_category_repository.get_category_by_id.assert_called_once_with(category_id)
    mock_category_repository.update_category.assert_called_once_with(existing_category, updated_data)
    assert result == updated_category

def test_update_category_not_found(category_service, mock_category_repository):
    category_id = "507f1f77bcf86cd799439011"
    updated_data = {"title": "Updated Title"}

    mock_category_repository.get_category_by_id.return_value = None

    result = category_service.update_category(category_id, updated_data)

    mock_category_repository.get_category_by_id.assert_called_once_with(category_id)
    mock_category_repository.update_category.assert_not_called()
    assert result is None

def test_delete_category_success(category_service, mock_category_repository):
    category_id = "507f1f77bcf86cd799439011"
    existing_category = {"id": category_id, "title": "Books"}

    mock_category_repository.get_category_by_id.return_value = existing_category
    mock_category_repository.delete_category.return_value = True

    result = category_service.delete_category(category_id)

    mock_category_repository.get_category_by_id.assert_called_once_with(category_id)
    mock_category_repository.delete_category.assert_called_once_with(existing_category)
    assert result is True

def test_delete_category_not_found(category_service, mock_category_repository):
    category_id = "507f1f77bcf86cd799439011"

    mock_category_repository.get_category_by_id.return_value = None

    result = category_service.delete_category(category_id)

    mock_category_repository.get_category_by_id.assert_called_once_with(category_id)
    mock_category_repository.delete_category.assert_not_called()
    assert result is False
