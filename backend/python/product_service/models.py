from mongoengine import Document, ReferenceField, StringField, FloatField, IntField
from product_category.models import ProductCategory

class Product(Document):
    name=StringField(required=True)
    description=StringField()
    category = ReferenceField(ProductCategory)
    price=FloatField(required=True)
    brand=StringField()
    quantity=IntField(required=True)

    