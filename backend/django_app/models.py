from mongoengine import Document, StringField, FloatField, IntField, DictField
from bson import DBRef, ObjectId


class ProductCategory(Document):
    """Model to store product categories"""
    title = StringField(required=True, unique=True)
    description = StringField()

    def to_dict(self):
        """Return category data as dictionary"""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
        }


class Product(Document):
    """Model to store products"""
    name = StringField(required=True)
    description = StringField()
    category = DictField()  # Storing DBRef and category data as dictionary
    price = FloatField(required=True)
    brand = StringField(required=True)
    quantity = IntField(required=True, min_value=0)

    def set_category(self, category):
        """Set category as DBRef and store metadata"""
        if isinstance(category, ProductCategory):
            self.category = {
                "_ref": DBRef("product_category", ObjectId(category.id)),
                "title": category.title,
                "description": category.description,
            }
        else:
            raise TypeError("Invalid category provided. Expected ProductCategory object.")

    def to_dict(self, fields=None):
        """Return product data with selected fields"""
        data = {}

        # Always include ID
        data["id"] = str(self.id)

        # Check if fields are specified and include only selected fields
        if not fields:
            fields = {"name", "description", "category", "price", "brand", "quantity"}

        if "name" in fields and hasattr(self, "name"):
            data["name"] = self.name
        if "description" in fields and hasattr(self, "description"):
            data["description"] = self.description
        if "category" in fields and hasattr(self, "category"):
            data["category"] = self.category if self.category else None
        if "price" in fields and hasattr(self, "price"):
            data["price"] = self.price
        if "brand" in fields and hasattr(self, "brand"):
            data["brand"] = self.brand
        if "quantity" in fields and hasattr(self, "quantity"):
            data["quantity"] = self.quantity

        return data

