from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ReferenceField, CASCADE
from django.utils import timezone
from django_app.models.category import Category

class Product(Document):
    name = StringField(required=True, max_length=100)

    category = ReferenceField(Category, reverse_delete_rule=CASCADE)

    description = StringField()
    price = FloatField(required=True, min_value=0.01)
    brand = StringField(required=True, max_length=100)
    quantity = IntField(required=True, min_value=0)

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

    meta = {'collection': 'products'}