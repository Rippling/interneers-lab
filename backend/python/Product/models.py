from mongoengine import (
    Document,
    StringField,
    FloatField,
    IntField,
    DateTimeField,
    ReferenceField,
)

"""
    Domain models for the inventory system.

    Week 4 changes:
      - ProductCategory is a new first-class entity with its own collection.
      - Product.category is now a ReferenceField to ProductCategory instead
        of a plain StringField.

    Image support:
      - Product.image_url is an optional URL string stored in MongoDB.
        The frontend renders it directly as an <img> src.
        For a dockerised setup the URL should be an http:// address reachable
        from the browser (e.g. a CDN URL or a path served by Django/nginx).
"""


class ProductCategory(Document):
    """
    Represents a product category in the inventory system.
    Stored in the 'product_categories' collection.
    """

    title = StringField(required=True, max_length=255)
    description = StringField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    meta = {"collection": "product_categories"}

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Product(Document):
    """
    Represents a product in the warehouse inventory.

    image_url — optional URL of the product image. Can be any http/https URL.
                If blank/None the frontend falls back to a placeholder.
    """

    name = StringField(required=True, max_length=255)
    description = StringField(required=True)
    category = ReferenceField(ProductCategory, required=False)
    price = FloatField(required=True)
    brand = StringField(required=True)
    quantity = IntField(required=True)
    # Optional product image URL stored in MongoDB
    image_url = StringField(required=False, default=None)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    meta = {"collection": "products"}

    def __str__(self):
        return f"{self.name} ({self.brand})"

    def to_dict(self):
        category_data = None
        if self.category:
            try:
                category_data = {
                    "id": str(self.category.id),
                    "title": self.category.title,
                }
            except Exception:
                category_data = {"id": str(self.category.id), "title": None}

        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": category_data,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity,
            "image_url": self.image_url or None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
