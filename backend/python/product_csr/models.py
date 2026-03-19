from mongoengine import (
    Document,
    StringField,
    FloatField,
    IntField,
    DateTimeField,
    ReferenceField
)
from datetime import datetime


class ProductCategory(Document):
    title = StringField(required=True, unique=True)
    description = StringField()
    
    meta = {
        "collection" : "product_categories"
    }
    
    def to_dict(self):
        return{
            "id": str(self.id),
            "title":self.title,
            "description": self.description
        }



class Product(Document):
    name = StringField(required=True)
    category = ReferenceField(ProductCategory)
    brand = StringField(required=True)
    price = FloatField()
    quantity = IntField()

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "products"
    }

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "category": str(self.category.id) if self.category else None,
            "brand": self.brand,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
