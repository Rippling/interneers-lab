from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ReferenceField
import datetime

class ProductCategory(Document):
    meta = {'collection': 'product_categories'}

    title = StringField(required=True, max_length=100, unique=True)
    description = StringField()
    
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(ProductCategory, self).save(*args, **kwargs)


class Product(Document):
    meta = {'collection': 'products'}

    name = StringField(required=True, max_length=255)
    description = StringField()
    price = FloatField(required=True, min_value=0.0)
    quantity = IntField(required=True, min_value=0)
    
    
    category = ReferenceField(ProductCategory, reverse_delete_rule=4) 
    brand = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(Product, self).save(*args, **kwargs)