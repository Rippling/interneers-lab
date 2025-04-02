from mongoengine import (
    Document,
    StringField,
    DecimalField,
    IntField,
    DateTimeField,
    signals,
)
from datetime import datetime, timezone


class Product(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = StringField(max_length=50)
    price = DecimalField(precision=2)
    brand = StringField(max_length=50)
    quantity = IntField(default=0, min_value=0)

    # Audit fields with timezone-aware datetime
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {"collection": "products_collection"}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        """Signal handler to update `updated_at` when the document is modified."""
        if document.id:
            document.updated_at = datetime.now(timezone.utc)


signals.pre_save.connect(Product.pre_save, sender=Product)
