import pytest
from bson import ObjectId

from products.services.product_service import ProductService
from products.exceptions import (
    InvalidProductId,
    ProductNotFound,
    InvalidCategoryId,
    CategoryNotFound
)

def test_create_product(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    data = {"name": "Laptop", "price": 1000}

    product_repo.create.return_value = data

    service = ProductService(product_repo, category_repo)

    result = service.create_product(data)

    assert result == data
    product_repo.create.assert_called_once_with(data)

def test_list_products(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    products = [{"name": "Laptop"}, {"name": "Phone"}]

    product_repo.get_all.return_value = products

    service = ProductService(product_repo, category_repo)

    result = service.list_products("-price")

    assert result == products
    product_repo.get_all.assert_called_once_with("-price")

def test_get_product_success(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    product_id = str(ObjectId())
    product = {"_id": product_id, "name": "Laptop"}

    product_repo.get_by_id.return_value = product

    service = ProductService(product_repo, category_repo)

    result = service.get_product(product_id)

    assert result == product        

def test_get_product_invalid_id(mocker):

    service = ProductService(mocker.Mock(), mocker.Mock())

    with pytest.raises(InvalidProductId):
        service.get_product("invalid-id")    


def test_get_product_not_found(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    product_repo.get_by_id.return_value = None

    service = ProductService(product_repo, category_repo)

    product_id = str(ObjectId())

    with pytest.raises(ProductNotFound):
        service.get_product(product_id) 

def test_update_product(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    product_id = str(ObjectId())

    product = mocker.Mock()
    product_repo.get_by_id.return_value = product
    product_repo.update.return_value = product

    service = ProductService(product_repo, category_repo)

    data = {"name": "Updated Laptop"}

    result = service.update_product(product_id, data)

    product_repo.update.assert_called_once_with(product)

def test_update_product_with_category(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    product_id = str(ObjectId())
    category_id = str(ObjectId())

    product = mocker.Mock()

    product_repo.get_by_id.return_value = product
    product_repo.update.return_value = product

    category = {"name": "Electronics"}
    category_repo.get_by_id.return_value = category

    service = ProductService(product_repo, category_repo)

    data = {"category": category_id}

    service.update_product(product_id, data)

    category_repo.get_by_id.assert_called_once_with(category_id) 

def test_delete_product(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    product_id = str(ObjectId())

    product = {"_id": product_id}

    product_repo.get_by_id.return_value = product

    service = ProductService(product_repo, category_repo)

    result = service.delete_product(product_id)

    product_repo.delete.assert_called_once_with(product_id)
    assert result == product

def test_list_products_by_category_id(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    products = [{"name": "Laptop"}]

    product_repo.get_all_by_category_id.return_value = products

    service = ProductService(product_repo, category_repo)

    result = service.list_products_by_category_id("cat123", "-price")

    assert result == products
    product_repo.get_all_by_category_id.assert_called_once_with("cat123", "-price")                          


def test_update_product_invalid_category_id(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    product_id = str(ObjectId())

    product_repo.get_by_id.return_value = mocker.Mock()

    service = ProductService(product_repo, category_repo)

    data = {"category": "invalid-id"}

    with pytest.raises(InvalidCategoryId):
        service.update_product(product_id, data)

def test_update_product_category_not_found(mocker):

    product_repo = mocker.Mock()
    category_repo = mocker.Mock()

    product_id = str(ObjectId())
    category_id = str(ObjectId())

    product_repo.get_by_id.return_value = mocker.Mock()
    category_repo.get_by_id.return_value = None

    service = ProductService(product_repo, category_repo)

    data = {"category": category_id}

    with pytest.raises(CategoryNotFound):
        service.update_product(product_id, data)        