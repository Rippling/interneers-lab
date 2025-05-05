from mongoengine import Document, StringField, ReferenceField, DateTimeField, DecimalField, IntField, BooleanField, ListField, UUIDField, CASCADE
from mongoengine.fields import EmbeddedDocumentField
from datetime import datetime
from decimal import Decimal
import uuid
from django.utils.text import slugify

class Category(Document):
    name = StringField(max_length=100, unique=True, required=True)
    slug = StringField(max_length=100, unique=True)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'categories',
        'ordering': ['name'],
        'indexes': ['name', 'slug']
    }

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)

    def __str__(self):
        return self.name

class Product(Document):
    STATUS_CHOICES = ('active', 'inactive', 'out_of_stock', 'discontinued')

    # Basic Information
    sku = StringField(max_length=50, unique=True, required=True)
    name = StringField(max_length=200, required=True)
    slug = StringField(max_length=200, unique=True)
    description = StringField()

    # Categorization
    category = ReferenceField(Category, reverse_delete_rule=CASCADE, required=True)
    brand = StringField(max_length=100)
    tags = ListField(StringField(max_length=50))

    # Pricing and Stock
    price = DecimalField(precision=2, min_value=Decimal('0.01'), required=True)
    discount_price = DecimalField(precision=2, min_value=Decimal('0.01'), required=False, null=True)
    quantity = IntField(min_value=0, required=True)
    low_stock_threshold = IntField(default=10, min_value=1)

    # Product Details
    weight = DecimalField(precision=2, required=False, null=True)
    dimensions = StringField(max_length=50)

    # Status and Tracking
    status = StringField(choices=STATUS_CHOICES, default='active')
    featured = BooleanField(default=False)
    rating = DecimalField(precision=2, min_value=Decimal('0.00'), max_value=Decimal('5.00'), required=False, null=True)

    # Metadata
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    uuid = UUIDField(binary=False, default=uuid.uuid4, unique=True)

    meta = {
        'collection': 'products',
        'ordering': ['-created_at'],
        'indexes': ['sku', 'name', 'status', 'brand']
    }

    def clean(self):
        if not self.slug:
            self.slug = slugify(self.name)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def is_in_stock(self):
        return self.quantity > 0

    @property
    def is_low_stock(self):
        return 0 < self.quantity <= self.low_stock_threshold
