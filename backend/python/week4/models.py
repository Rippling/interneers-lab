from datetime import datetime
from mongoengine import Document, SequenceField, StringField, DecimalField, IntField, DateTimeField, ReferenceField, NULLIFY

# one category can contain many products but one product belongs to one category


# this represents a category like food, kitchen essentials, electornics, etc
class ProductCategory(Document):
    id = SequenceField(primary_key=True)
    # no 2 category should have same title
    title = StringField(required=True, unique=True, max_length=100)
    description = StringField(default="", max_length=300)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    # just like week3 this tells mongoengine which mongodb collection name to use
    meta = {
        "collection": "week4_product_categories"
    }

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


# this represents actual product like TV, fridge, rice, etc
class Product(Document):
    id = SequenceField(primary_key=True)
    name = StringField(required=True, max_length=200)
    description = StringField(required=True)
    price = DecimalField(required=True, precision=2, min_value=0)
    # at model level, brand is optional because old products may already exist without brand
    # if model makes it compulsary then old record may cause problems
    # for new products we have enforced rules in serializer and service
    brand = StringField(required=False, max_length=100, default="")
    quantity = IntField(required=True, min_value=0)
    # reverse delete rule = null bcz if ref category is deleted do not delete product
    category = ReferenceField(
        ProductCategory, required=False, null=True, reverse_delete_rule=NULLIFY)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "week4_products"
    }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "brand": self.brand,
            "quantity": self.quantity,
            "category": self.category.to_dict() if self.category else None,
            "category_id": self.category.id if self.category else None,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
