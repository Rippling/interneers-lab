from mongoengine import Document, StringField, FloatField, IntField, DateField, DateTimeField
from datetime import datetime
import pytz

class Product(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    category = StringField(required=True)
    price_in_RS = FloatField(required=True, default=0.0)
    brand = StringField()
    quantity = IntField(required=True)
    manufacture_date = DateField(required=True)
    expiry_date = DateField(required=True)
    weight_in_KG = FloatField(default=0.0)

# These fields will be helpful when filtering will be done futher and in sorting of products as well
    created_at = DateTimeField(default=lambda: datetime.now(pytz.utc))  # Stored in UTC format in MongoDB
    updated_at = DateTimeField(default=lambda: datetime.now(pytz.utc))

    meta = {
        "collection": "products",
        "indexes": ["name", "category", "price_in_RS", "brand"],
    }

    def save(self, *args, **kwargs):
        """Ensure updated_at is changed only when modifying the document."""
        if self.pk:  # If document already exists, update only updated_at
            self.updated_at = datetime.now(pytz.utc)
        else:  # If it's a new document, set created_at
            self.created_at = datetime.now(pytz.utc)

        super(Product, self).save(*args, **kwargs)
