from mongoengine import Document, ReferenceField, StringField, DecimalField, IntField, DateTimeField
from datetime import datetime

class ProductCategory(Document):
    title = StringField(required=True, unique=True, max_length=100)
    description = StringField()

    meta = {'collection': 'product_categories'}

class Product(Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    category = ReferenceField(ProductCategory, reverse_delete_rule=3)
    price = DecimalField(precision=2, required=True)
    brand = StringField(max_length=50, required=True)
    quantity_in_warehouse = IntField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'products'} 

    def save(self, *args, **kwargs):
        """Override save method to update timestamp."""
        self.updated_at = datetime.utcnow()  # Update timestamp on save
        return super(Product, self).save(*args, **kwargs)
