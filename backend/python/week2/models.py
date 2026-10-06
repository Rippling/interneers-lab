from django.db import models
from decimal import Decimal


class Product:
    def __init__(self, id, name, description, category, price, brand, quantity):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = Decimal(str(price))
        self.brand = brand
        self.quantity = quantity

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": str(self.price),
            "brand": self.brand,
            "quantity": self.quantity,
        }
