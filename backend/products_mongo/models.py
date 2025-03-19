from mongoengine import Document, StringField, DecimalField, IntField, DateTimeField
from datetime import datetime

class Product(Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    category = StringField(max_length=50)
    price = DecimalField(precision=2, required=True)
    brand = StringField(max_length=50)
    quantity_in_warehouse = IntField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'products'} 

    def save(self, *args, **kwargs):
        """Override save method to update timestamp."""
        self.updated_at = datetime.utcnow()  # Update timestamp on save
        return super(Product, self).save(*args, **kwargs)
