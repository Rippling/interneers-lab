from datetime import datetime

from mongoengine import (
    DateTimeField,
    Document,
    FloatField,
    IntField,
    ReferenceField,
    StringField,
    ValidationError,
)


class ProductCategory(Document):
    title = StringField(required=True)
    description = StringField(default="")
    owner_id = StringField(required=True)

    meta = {
        "collection": "product_categories",
    }

    def clean(self):
        if not self.title or not self.title.strip():
            raise ValidationError("Title is required")

        self.title = self.title.strip()
        self.description = self.description.strip() if self.description else ""

        if not self.owner_id or not self.owner_id.strip():
            raise ValidationError("Owner is required")

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "owner_id": self.owner_id,
        }


class Product(Document):
    name = StringField(required=True)
    category = ReferenceField(ProductCategory, required=False)
    brand = StringField(required=True)
    price = FloatField(required=True)
    quantity = IntField(required=True)
    description = StringField(default="")
    image_url = StringField(default="")
    owner_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "products",
    }

    def clean(self):
        if not self.name or not self.name.strip():
            raise ValidationError("name is required")

        if not self.brand or not self.brand.strip():
            raise ValidationError("brand is required")

        if self.price is None:
            raise ValidationError("price is required")

        if self.price <= 0:
            raise ValidationError("Price must be positive")

        if self.quantity is None:
            raise ValidationError("quantity is required")

        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")

        if not self.owner_id or not self.owner_id.strip():
            raise ValidationError("Owner is required")

        self.name = self.name.strip()
        self.brand = self.brand.strip()
        self.description = self.description.strip() if self.description else ""
        self.image_url = self.image_url.strip() if self.image_url else ""

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "category": str(self.category.id) if self.category else None,
            "brand": self.brand,
            "price": self.price,
            "quantity": self.quantity,
            "description": self.description,
            "image_url": self.image_url,
            "owner_id": self.owner_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
