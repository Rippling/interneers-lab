from mongoengine import Document, StringField, IntField

class Product(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = StringField(max_length=60)
    price = IntField(required=True)
    brand = StringField(max_length=60)
    quantity = IntField()

    def __str__(self):
        return self.name
