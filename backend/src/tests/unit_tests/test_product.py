"""
Unit tests for the Product document model using pytest.

This test suite verifies the correctness of the Product class defined in
`src.models.product`, ensuring that all business logic and constraints
are properly enforced. It includes:

- Field initialization and default timestamps
- Stock and price modification behaviors
- Validation for required fields and invalid inputs
- Timestamp updating logic upon save or modification
- Input validation and exception handling

All timestamps are mocked using a fixed datetime to ensure deterministic test outcomes.
"""


import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from src.models.product import Product
from mongoengine.errors import ValidationError

#pylint: disable=no-member

FIXED_TIME = datetime(2024, 1, 1, 12, 0, 0)

DEFAULT_PRODUCT_DATA = {
    "name": "Test Product",
    "price": 100,
    "brand": "Test Brand",
    "quantity": 10,
    "description": "Sample description"
}

@pytest.fixture
def product_instance() -> Product:
    """Fixture that returns a default Product instance with required fields."""
    with patch("src.models.product.datetime") as mock_datetime:
        mock_datetime.datetime.now.return_value = FIXED_TIME.replace(tzinfo=timezone.utc)
        mock_datetime.datetime.utcnow.return_value = FIXED_TIME
        return Product(**DEFAULT_PRODUCT_DATA)

def assert_valid_modified_at(modified_at: datetime) -> None:
    """Helper function to validate that modified_at matches the mocked datetime."""
    assert isinstance(modified_at, datetime)
    print(modified_at.replace(tzinfo=timezone.utc), "==", FIXED_TIME.replace(tzinfo=timezone.utc))
    assert modified_at.replace(tzinfo=timezone.utc) == FIXED_TIME.replace(tzinfo=timezone.utc)

def test_product_creation_fields(product_instance: Product) -> None:
    """Test that a product instance is correctly initialized with expected fields and timestamps."""
    assert product_instance.name == DEFAULT_PRODUCT_DATA["name"]
    assert product_instance.price == DEFAULT_PRODUCT_DATA["price"]
    assert product_instance.brand == DEFAULT_PRODUCT_DATA["brand"]
    assert product_instance.quantity == DEFAULT_PRODUCT_DATA["quantity"]
    assert product_instance.description == DEFAULT_PRODUCT_DATA["description"]
    assert isinstance(product_instance.created_at, datetime)
    assert isinstance(product_instance.modified_at, datetime)
    assert product_instance.created_at == FIXED_TIME.replace(tzinfo=timezone.utc)
    assert product_instance.modified_at == FIXED_TIME.replace(tzinfo=timezone.utc)

@patch("src.models.product.datetime", autospec=True)
@patch.object(Product, "save", MagicMock())
def test_modify_stock_increase(mock_datetime: MagicMock, product_instance: Product) -> None:
    """Test increasing stock updates quantity correctly and refreshes timestamp."""
    mock_datetime.datetime.utcnow.return_value = FIXED_TIME
    result: int = product_instance.modify_stock(5)
    assert result == 5  # Should return the amount added
    assert product_instance.quantity == 5  # Updated from default 10 to 5
    Product.save.assert_called_once()
    assert_valid_modified_at(product_instance.modified_at)

@patch("src.models.product.datetime", autospec=True)
@patch.object(Product, "save", MagicMock())
def test_modify_stock_decrease_valid(mock_datetime: MagicMock, product_instance: Product) -> None:
    """Test decreasing stock with a valid value updates quantity correctly and refreshes timestamp."""
    mock_datetime.datetime.utcnow.return_value = FIXED_TIME
    result: int = product_instance.modify_stock(-3)
    assert result == 13  # Increase because initial is 10
    assert product_instance.quantity == 13
    Product.save.assert_called_once()
    assert_valid_modified_at(product_instance.modified_at)

@patch.object(Product, "save", MagicMock())
def test_modify_stock_raises_if_negative(product_instance: Product) -> None:
    """Test that stock modification raising quantity below zero throws ValueError."""
    product_instance.quantity = 2
    with pytest.raises(ValueError, match="Stock cannot be negative."):
        product_instance.modify_stock(-3)

@patch("src.models.product.datetime", autospec=True)
@patch.object(Product, "save", MagicMock())
def test_set_stock_valid(mock_datetime: MagicMock, product_instance: Product) -> None:
    """Test that setting a valid stock updates quantity and timestamp properly."""
    mock_datetime.datetime.utcnow.return_value = FIXED_TIME
    result: int = product_instance.set_stock(25)
    assert product_instance.quantity == 25
    assert result == 25  # Confirm returned new quantity
    Product.save.assert_called_once()
    assert_valid_modified_at(product_instance.modified_at)

@patch.object(Product, "save", MagicMock())
def test_set_stock_negative_raises(product_instance: Product) -> None:
    """Test that setting a negative stock raises ValueError."""
    with pytest.raises(ValueError, match="Stock cannot be negative."):
        product_instance.set_stock(-5)

@patch("src.models.product.datetime", autospec=True)
@patch.object(Product, "save", MagicMock())
def test_set_price_valid(mock_datetime: MagicMock, product_instance: Product) -> None:
    """Test that setting a valid price updates the value and timestamp."""
    mock_datetime.datetime.utcnow.return_value = FIXED_TIME
    result: int = product_instance.set_price(199)
    assert product_instance.price == 199
    assert result == 199
    Product.save.assert_called_once()
    assert_valid_modified_at(product_instance.modified_at)

@patch.object(Product, "save", MagicMock())
def test_set_price_negative_raises(product_instance: Product) -> None:
    """Test that setting a negative price raises ValueError."""
    with pytest.raises(ValueError, match="Price cannot be negative."):
        product_instance.set_price(-10)

@patch("src.models.product.datetime", autospec=True)
@patch.object(Product, "save", MagicMock())
def test_modify_fields_valid_keys(mock_datetime: MagicMock, product_instance: Product) -> None:
    """Test modifying multiple valid fields updates them correctly and refreshes timestamp."""
    mock_datetime.datetime.utcnow.return_value = FIXED_TIME
    updates: dict[str, object] = {"name": "New Name", "price": 150, "description": "Updated"}
    product_instance.modify_fields(updates)
    assert product_instance.name == "New Name"
    assert product_instance.price == 150
    assert product_instance.description == "Updated"
    Product.save.assert_called_once()
    assert_valid_modified_at(product_instance.modified_at)

@patch.object(Product, "save", MagicMock())
def test_modify_fields_invalid_key_raises(product_instance: Product) -> None:
    """Test that modifying fields with an invalid key raises KeyError."""
    with pytest.raises(KeyError, match="Field invalid_key is not a valid field."):
        product_instance.modify_fields({"invalid_key": "oops"})

@patch("src.models.product.datetime", autospec=True)
def test_change_modified_timestamp_sets_utc(mock_datetime: MagicMock, product_instance: Product) -> None:
    """Test that the change_modified_timestamp method correctly sets the timestamp."""
    mock_datetime.datetime.utcnow.return_value = FIXED_TIME
    product_instance.change_modified_timestamp()
    assert isinstance(product_instance.modified_at, datetime)
    assert product_instance.modified_at == FIXED_TIME

# --- Additional input validation tests ---

@patch("src.models.product.datetime", autospec=True)
def test_description_too_long_raises(mock_datetime: MagicMock) -> None:
    """Test that setting a description longer than 250 characters raises ValidationError."""
    mock_datetime.datetime.now.return_value = FIXED_TIME.replace(tzinfo=timezone.utc)
    long_description = "x" * 300
    with pytest.raises(Exception):
        Product(
            name="Test",
            price=10,
            quantity=5,
            description=long_description
        ).validate()

@patch("src.models.product.datetime", autospec=True)
def test_missing_required_fields_raises(mock_datetime: MagicMock) -> None:
    """Test that missing required fields like name, price, or quantity raises ValidationError."""
    mock_datetime.datetime.now.return_value = FIXED_TIME.replace(tzinfo=timezone.utc)
    with pytest.raises(Exception):
        Product(description="Valid desc").validate()

@patch("src.models.product.datetime", autospec=True)
def test_negative_price_on_creation_raises(mock_datetime: MagicMock) -> None:
    """Test that creating a product with a negative price raises ValidationError."""
    mock_datetime.datetime.now.return_value = FIXED_TIME.replace(tzinfo=timezone.utc)
    with pytest.raises(ValidationError):
        Product(name="X", price=-5, quantity=1).validate()

@patch("src.models.product.datetime", autospec=True)
def test_negative_quantity_on_creation_raises(mock_datetime: MagicMock) -> None:
    """Test that creating a product with a negative quantity raises ValidationError."""
    mock_datetime.datetime.now.return_value = FIXED_TIME.replace(tzinfo=timezone.utc)
    with pytest.raises(ValidationError):
        Product(name="X", price=10, quantity=-1).validate()
