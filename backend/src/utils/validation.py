from src.models.product_category import ProductCategory
from mongoengine.errors import ValidationError, DoesNotExist

#pylint: disable=no-member

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
        ProductCategory.objects.get(title= category_title)
    except DoesNotExist as e:
        raise ValidationError("Category does not exist in the database.") from e