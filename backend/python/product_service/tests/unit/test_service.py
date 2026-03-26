import pytest
from unittest.mock import patch

from product_service.services import ProductServices

@patch("product_service.services.ProductRepository")
def test_create_product(mock_repo):

    data = {
        "name": "Apple",
        "description": "Fresh red apple",
        "price": 10.0,
        "brand": "Test Brand",
        "quantity": 5
    }

    mock_repo.create.return_value = data
    
    result = ProductServices.create_product(data)
    assert result["name"] == data["name"]
    mock_repo.create.assert_called_once_with(data)

@patch("product_service.services.ProductRepository")
def test_create_product_with_invalid_price(mock_repo):        
    data = {
        "name": "Apple",
        "description": "Fresh red apple",
        "price": -5.0,
        "brand": "Test Brand",
        "quantity": 5
    }

    with pytest.raises(ValueError) as excinfo:
        ProductServices.create_product(data)
    
    assert str(excinfo.value) == "Given Price is not valid"
    mock_repo.create.assert_not_called()

@patch("product_service.services.ProductRepository")
def test_get_product_by_id(mock_repo):
    product_id = "12345"
    expected_product = {
        "id": product_id,
        "name": "Apple",
        "description": "Fresh red apple",
        "price": 10.0,
        "brand": "Test Brand",
        "quantity": 5
    }

    mock_repo.get_by_id.return_value = expected_product

    result = ProductServices.get_product(product_id)
    assert result["id"] == expected_product["id"]
    mock_repo.get_by_id.assert_called_once_with(product_id)

@patch("product_service.services.ProductRepository")
def test_get_product_by_id_not_found(mock_repo):
    product_id = "12345"
    mock_repo.get_by_id.return_value = None

    with pytest.raises(ValueError) as excinfo:
        ProductServices.get_product(product_id)
    
    assert str(excinfo.value) == "Product not found"
    mock_repo.get_by_id.assert_called_once_with(product_id)

@patch("product_service.services.ProductRepository")
def test_list_products_by_category_id(mock_repo):
    category_id = "cat123"
    expected_products = [
        {
            "id": "prod1",
            "name": "Apple",
            "description": "Fresh red apple",
            "price": 10.0,
            "brand": "Test Brand",
            "quantity": 5
        },
        {
            "id": "prod2",
            "name": "Banana",
            "description": "Ripe yellow banana",
            "price": 5.0,
            "brand": "Test Brand",
            "quantity": 10
        }
    ]

    mock_repo.get_all_by_category_id.return_value = expected_products

    result = ProductServices.list_products_by_category_id(category_id)
    assert len(result) == len(expected_products)
    mock_repo.get_all_by_category_id.assert_called_once_with(category_id)   

@patch("product_service.services.ProductRepository")
def test_add_category_to_product(mock_repo):
    #  category_id and product_id  should be a valid ObjectId, it must be a 12-byte input
    product_id = "0000000000000000000000000"
    category_id = "0000000000000000000000000"
    expected_product = {
        "id": product_id,
        "name": "Apple",
        "description": "Fresh red apple",
        "price": 10.0,
        "brand": "Test Brand",
        "quantity": 5,
        "category": category_id
    }

    mock_repo.add_category_to_product.return_value = expected_product

    result = ProductServices.add_category_to_product(product_id, category_id)
    assert result["category"] == expected_product["category"]
    mock_repo.add_category_to_product.assert_called_once_with(product_id, category_id)         

def test_add_category_to_product_not_found():
    with patch("product_service.services.ProductRepository") as mock_repo:
        product_id = "0000000000000000000000000"
        category_id = "000000000000000000000000"
        mock_repo.add_category_to_product.return_value = None

        with pytest.raises(ValueError) as excinfo:
            ProductServices.add_category_to_product(product_id, category_id)
        
        assert str(excinfo.value) == "Product not found"
        mock_repo.add_category_to_product.assert_called_once_with(product_id, category_id)

@patch("product_service.services.ProductRepository")
def test_remove_category_from_product(mock_repo):
    product_id = "prod123"
    expected_product = {
        "id": product_id,
        "name": "Apple",
        "description": "Fresh red apple",
        "price": 10.0,
        "brand": "Test Brand",
        "quantity": 5,
        "category": None
    }

    mock_repo.remove_category_from_product.return_value = expected_product

    result = ProductServices.remove_category_from_product(product_id)
    assert result["category"] is None
    mock_repo.remove_category_from_product.assert_called_once_with(product_id)    

