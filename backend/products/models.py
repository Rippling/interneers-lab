from mongoengine import (
    Document,
    StringField,
    DecimalField,
    IntField,
    DateTimeField,
    ReferenceField,
    CASCADE,
    signals,
)
from datetime import datetime, timezone

class ProductCategory(Document):
    title = StringField(max_length=200,unique = True, required = True)
    description = StringField()

    meta = {"collection": "product_categories_collection"}

    def __str__(self):
        return self.title

class Product(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = ReferenceField("ProductCategory", reverse_delete_rule=CASCADE)
    price = DecimalField(precision=2)
    brand = StringField(max_length=50, required=True)
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