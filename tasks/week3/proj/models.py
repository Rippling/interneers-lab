from mongoengine import Document, StringField, FloatField, IntField, ReferenceField

#week 3
# class Product(Document):
#     name = StringField(required=True, max_length=100)
#     description = StringField()
#     category = StringField(max_length=50)
#     price = FloatField(required=True) 
#     brand = StringField(max_length=50)
#     quantity = IntField(required=True) 



#week4
class ProductCategory(Document):
    title = StringField(required=True, max_length=100)
    description = StringField()

class Product(Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    price = FloatField(required=True) 
    quantity = IntField(required=True) 
    
    # Requirement 5: Brand is now strictly required
    brand = StringField(required=True, max_length=50) 
    
    # Requirement 2: Model products belonging to a category
    category = ReferenceField(ProductCategory)