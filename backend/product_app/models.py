from django.db import models
import mongoengine as me
from datetime import datetime

class Product(me.Document):
    name = me.StringField(max_length=255)
    description = me.StringField(blank=True, null=True)
    category = me.StringField(max_length=100)
    price = me.FloatField()
    brand = me.StringField(max_length=100)
    quantity = me.IntField()
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'products'}
    # def __str__(self):
    #     return self.name
