from mongoengine import Document, StringField, FloatField

class Product(Document):
    name=StringField(required=True)
    description=StringField()
    price=FloatField(required=True)
    