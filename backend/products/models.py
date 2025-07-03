# from django.db import models
from mongoengine import Document
from mongoengine import StringField, IntField, DateTimeField, ObjectIdField
from mongoengine import ReferenceField, ListField, CASCADE

import datetime

class ProductCategory(Document):


    meta = {'collection': 'product_category'}  # Specify the collection name in MongoDB
    category_id = IntField(required=True,unique=True)
    category_name = StringField(required=True) 
    
    # product_list = ListField(ReferenceField(Products))
    description = StringField()

    def __str__(self):
        return self.category_name

class Products(Document):
    meta = {'collection': 'products'}  # Specify the collection name in MongoDB

    product_id = IntField(required=True,unique=True)
    name = StringField(max_length=100, required=True)
    description = StringField()
    category = ReferenceField(ProductCategory, reverse_delete_rule=CASCADE)
    brand=StringField(max_length=100, required=True) 
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(Products, self).save(*args, **kwargs)



# Create your models here.
