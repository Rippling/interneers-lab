import datetime
from mongoengine import Document, ReferenceField, StringField, FloatField, IntField, DateTimeField, NULLIFY


class Category(Document):
    name=StringField(required=True)
    description=StringField()     
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    
    def save(self, *args, **kwargs):

        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)      

    

    
class Product(Document):
    name=StringField(required=True)
    description=StringField()
    category = ReferenceField(Category,reverse_delete_rule=NULLIFY) # reverse_delete_rule=NULLIFY
    price=FloatField(required=True)
    brand=StringField(required=True)
    quantity=IntField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):

        self.updated_at = datetime.datetime.now()
        return super().save(*args, **kwargs)
    
    

