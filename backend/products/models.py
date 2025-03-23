from mongoengine import Document, StringField, DecimalField, IntField

class Product(Document):
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = StringField(max_length=50)
    price = DecimalField(precision=2)  
    brand = StringField(max_length=50)
    quantity = IntField(default=0, min_value=0)  

    meta = {
        'collection': 'products_collection'
    }