from mongoengine import Document, ReferenceField, StringField, FloatField, IntField
from product_category.models import ProductCategory



class Product(Document):
    name=StringField(required=True)
    description=StringField()
    category = ReferenceField(ProductCategory)
    price=FloatField(required=True)
    brand=StringField(required=True)
    quantity=IntField(required=True)

    def clean(self):
        if not self.brand or self.brand.strip() == "":
            raise ValueError("Brand cannot be empty or whitespace")

    