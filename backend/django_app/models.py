from mongoengine import Document, StringField, FloatField, IntField

class Product(Document):
    name = StringField(required=True)
    description = StringField()
    category = StringField(required=True)
    price = FloatField(required=True)
    brand = StringField()
    quantity = IntField(required=True)
