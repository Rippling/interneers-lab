import pytest
from product.services.product_service import ProductService
from product.repositories.product_repository import ProductRepository

@pytest.fixture
def mock_product_repository(mocker):
    return mocker.MagicMock(spec=ProductRepository)

@pytest.fixture
def product_service(mock_product_repository, mocker):
    # Patch the ProductRepository inside the ProductService to use the mock
    mocker.patch(
        "product.services.product_service.ProductRepository",
        return_value=mock_product_repository
    )
    return ProductService()

# Test for successful product creation
def test_create_product_success(product_service, mock_product_repository):
    data = {
        "name": "Harry Potter and the Philosopher's Stone",
        "category": "Book",
        "price_in_RS": 6000,
        "quantity": 5,
        "manufacture_date": "2024-01-01",
        "expiry_date": "2026-01-01",
        "brand" : "Penguin",
    }
    mock_product_repository.create_product.return_value = data

    result = product_service.create_product(data)

    mock_product_repository.create_product.assert_called_once_with(data)
    assert result == data

# Test product creation failure (in case of missing fields)
def test_create_product_missing_field(product_service):
    data = {
        "name": "Harry Potter and the Philosopher's Stone",
        "price_in_RS": 60000 
    }
    with pytest.raises(ValueError, match="brand is required."):
        product_service.create_product(data)

#  Test fetching products by category
def test_get_filtered_products_success(product_service, mock_product_repository):
    category_name = "Book"
    mock_products = [{"name": "Harry Potter and the Philosopher's Stone", "category": "Book"}]
    mock_product_repository.get_products_by_category.return_value = (mock_products, None)

    products, error = product_service.get_filtered_products(category_name)

    mock_product_repository.get_products_by_category.assert_called_once_with(category_name)
    assert products == mock_products
    assert error is None

def test_get_filtered_products_error(product_service, mock_product_repository):
    category_name = "Book"
    mock_product_repository.get_products_by_category.return_value = (None, "Database Error")

    products, error = product_service.get_filtered_products(category_name)

    assert products is None
    assert error == "Database Error"

# Test getting product by ID
def test_get_product_by_id_success(product_service, mock_product_repository):
    product_id = "1234"
    mock_product = {"id": "1234", "name": "Harry Potter and the Philosopher's Stone"}
    mock_product_repository.get_product_by_id.return_value = mock_product

    product, error = product_service.get_product_by_id(product_id)

    mock_product_repository.get_product_by_id.assert_called_once_with(product_id)
    assert product == mock_product
    assert error is None

def test_get_product_by_id_not_found(product_service, mock_product_repository):
    product_id = "1000"
    mock_product_repository.get_product_by_id.return_value = None

    product, error = product_service.get_product_by_id(product_id)

    assert product is None
    assert error == "Product not found."

# Test deleting a product
def test_delete_product_success(product_service, mock_product_repository):
    product_id = "123"
    mock_product_repository.get_product_by_id.return_value = {"id": "123", "name": "Harry Potter and the Philosopher's Stone"}
    mock_product_repository.delete_product.return_value = True

    result = product_service.delete_product(product_id)

    mock_product_repository.delete_product.assert_called_once_with(product_id)
    assert result is True

def test_delete_product_not_found(product_service, mock_product_repository):
    product_id = "999"
    mock_product_repository.get_product_by_id.return_value = None

    with pytest.raises(ValueError, match = "Product not found at service layer"):
        product_service.delete_product(product_id)

def test_update_product_success(product_service, mock_product_repository):
    product_id = "123"
    update_data = {"name": "Harry Potter and the Half blood prince"}
    mock_product_repository.get_product_by_id.return_value = {"id": "123", "name": "Harry Potter and the Half blood prince"}
    mock_product_repository.update_product.return_value = {"id": "123", "name": "Harry Potter and the Half blood prince"}

    result = product_service.update_product(product_id, update_data)

    mock_product_repository.update_product.assert_called_once_with(product_id, update_data)
    assert result["name"] == "Harry Potter and the Half blood prince"

def test_update_product_not_found(product_service, mock_product_repository):
    product_id = "999"
    update_data = {"name": "Updated"}
    mock_product_repository.get_product_by_id.return_value = None

    with pytest.raises(ValueError, match="Product not found"):
        product_service.update_product(product_id, update_data)

def test_update_product_attempt_to_update_id(product_service, mock_product_repository):
    product_id = "123"
    update_data = {"id": "new_id", "name": "Updated"}
    mock_product_repository.get_product_by_id.return_value = {"id": "123", "name": "Old"}

    with pytest.raises(ValueError, match="Updating the product ID is not allowed"):
        product_service.update_product(product_id, update_data)

def test_add_category_to_product(product_service, mock_product_repository):
    product_id = "123"
    category_id = "cat456"
    mock_product_repository.add_category_to_product.return_value = True

    result = product_service.add_category_to_product(product_id, category_id)

    mock_product_repository.add_category_to_product.assert_called_once_with(product_id, category_id)
    assert result is True

def test_remove_category_from_product(product_service, mock_product_repository):
    product_id = "123"
    category_id = "cat456"
    mock_product_repository.remove_category_from_product.return_value = True

    result = product_service.remove_category_from_product(product_id, category_id)

    mock_product_repository.remove_category_from_product.assert_called_once_with(product_id, category_id)
    assert result is True
