from src.services.product_category_service import ProductCategoryService
from mongoengine.errors import ValidationError, DoesNotExist

def validate_category(category_title: str):
    """
    Validates if the input string is a valid category title.

    Args:
        - category_title: the input to be validated
    Raises:
        ValidationError if title is not a string, or the category corresponding to this
        title is not in the database.
    """
    if not isinstance(category_title, str):
        raise ValidationError("Category title must be a string.")
    try:
        ProductCategoryService.get_category_by_title(category_title)
    except DoesNotExist as e:
        raise ValidationError("Category does not exist in the database.") from e