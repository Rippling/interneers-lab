from mongoengine import Document,fields
from datetime import datetime,timezone

#model for defining category of a prod.(reference to the Product model)
class ProductCategory(Document):
    title=fields.StringField(required=True,max_length=100,unique=True)
    description=fields.StringField(max_length=500)
    created_at=fields.DateTimeField(default=datetime.now(timezone.utc))
    updated_at=fields.DateTimeField(default=datetime.now(timezone.utc))

    meta={
        'collection': 'product_categories',
        'ordering': ['-created_at']
    }

    def save(self, *args, **kwargs):
        self.updated_at=datetime.now(timezone.utc)
        return super(ProductCategory, self).save(*args, **kwargs)