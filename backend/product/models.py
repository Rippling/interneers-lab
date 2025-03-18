from mongoengine import Document, StringField, FloatField, IntField, DateField

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

    meta = {
        "collection": "products",
        "indexes": ["name", "category", "price_in_RS", "brand"]
    }
