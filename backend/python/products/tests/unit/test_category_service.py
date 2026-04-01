import pytest
from bson import ObjectId

from products.services.category_service import CategoryService
from products.exceptions import (
    InvalidCategoryId,
    CategoryNotFound
)

def test_create_category(mocker):

    repo = mocker.Mock()

    data = {"name": "Electronics"}

    repo.create.return_value = data

    service = CategoryService(repo)

    result = service.create_category(data)

    assert result == data
    repo.create.assert_called_once_with(data)

def test_get_all_categories(mocker):

    repo = mocker.Mock()

    categories = [
        {"name": "Electronics"},
        {"name": "Books"}
    ]

    repo.get_all.return_value = categories

    service = CategoryService(repo)

    result = service.get_all_categories()

    assert result == categories
    repo.get_all.assert_called_once()

def test_get_category_success(mocker):

    repo = mocker.Mock()

    category_id = str(ObjectId())
    category = {"_id": category_id, "name": "Electronics"}

    repo.get_by_id.return_value = category

    service = CategoryService(repo)

    result = service.get_category(category_id)

    assert result == category

def test_get_category_invalid_id(mocker):

    service = CategoryService(mocker.Mock())

    with pytest.raises(InvalidCategoryId):
        service.get_category("invalid-id")

def test_get_category_not_found(mocker):

    repo = mocker.Mock()

    repo.get_by_id.return_value = None

    service = CategoryService(repo)

    category_id = str(ObjectId())

    with pytest.raises(CategoryNotFound):
        service.get_category(category_id)

def test_update_category(mocker):

    repo = mocker.Mock()

    category_id = str(ObjectId())

    category = mocker.Mock()

    repo.get_by_id.return_value = category
    repo.update.return_value = category

    service = CategoryService(repo)

    data = {"name": "Updated Category"}

    result = service.update_category(category_id, data)

    repo.update.assert_called_once_with(category)
    assert result == category

def test_delete_category(mocker):

    repo = mocker.Mock()

    category_id = str(ObjectId())

    category = {"_id": category_id}

    repo.get_by_id.return_value = category

    service = CategoryService(repo)

    result = service.delete_category(category_id)

    repo.delete.assert_called_once_with(category_id)
    assert result == category                                