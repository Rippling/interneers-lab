from mongoengine import Document, StringField, DateTimeField
from django.utils import timezone

class Category(Document):
    title = StringField(required=True, max_length=100)
    description = StringField()

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

    meta = {'collection': 'categories'}

    