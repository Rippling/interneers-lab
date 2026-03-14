from mongoengine import Document, StringField

class ProductCategory(Document):
    name = StringField(required=True)
    description = StringField()