from datetime import datetime
from mongoengine import Document, SequenceField, StringField, DecimalField, IntField, DateTimeField


class Product(Document):
    # seq field is used for auto incrementing numeric id's
    id = SequenceField(primary_key=True)
    name = StringField(required=True, max_length=200)
    description = StringField(required=True)
    category = StringField(required=True, max_length=100)
    price = DecimalField(required=True, precision=2, min_value=0)
    brand = StringField(max_length=100, default="")
    quantity = IntField(required=True, min_value=0)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    # you are telling MongoEngine to put all Product objects inside the products folder/bucket
    meta = {
        "collection": "products"
    }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": str(self.price),
            "brand": self.brand,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
