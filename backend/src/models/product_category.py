
import datetime
from mongoengine import Document, StringField

class ProductCategory(Document):
    """
    Represents a category of products.

    Each category has a title and an optional description.
    """
    title = StringField(required=True, unique=True)
    description = StringField(max_length=250)