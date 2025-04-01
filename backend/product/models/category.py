from mongoengine import Document, StringField, DateTimeField, BooleanField
from datetime import datetime
import pytz
class ProductCategory(Document):
    category_name = StringField(required=True, unique=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.now(pytz.utc))  
    updated_at = DateTimeField(default=datetime.now(pytz.utc))  
    is_active = BooleanField(default=True) 

    meta = {
        'collection': 'product_categories',
        'ordering': ['-created_at']  
    }

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        """Override save method to update `updated_at` field on modification."""
        self.updated_at = datetime.now(pytz.utc)
        super(ProductCategory, self).save(*args, **kwargs)
