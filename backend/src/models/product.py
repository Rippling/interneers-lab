"""
Product document schema (and associated managing functions)
{
    name: <str> (required) 
    price: <int> (required) [0,inf)
    brand: <str>
    quantity: <int> (required) [0,inf)
    description: <str> [max length= 250]
    created_at: <datetime.datetime> (automatic)
    modified_at; <datetime.datetime> (automatic)
}
"""

import datetime
from mongoengine import Document, StringField, IntField, DateTimeField
from mongoengine.errors import ValidationError, DoesNotExist

from src.utils.validation import validate_category

class Product(Document):
    name= StringField(required= True)
    price= IntField(required= True)
    brand= StringField()
    quantity= IntField(required= True)
    description= StringField(max_length= 250)
    category= StringField(max_length= 250, validation= validate_category)

    created_at= DateTimeField(default= lambda: datetime.datetime.now(datetime.timezone.utc))
    modified_at= DateTimeField(default= lambda: datetime.datetime.now(datetime.timezone.utc))

    def modify_stock(self, amount: int):
        """
        Updates the product stock by increasing its quantity by the specified amount (integer).

        Ensures that stock does not become negative after modification.

        Args:
            amount: int value to adjust stock by (positive to increase, negative to decrease).

        Returns:
            Updated stock quantity as an int.

        Raises:
            ValueError: If modification results in a negative stock quantity.
        """
        if self.quantity+ amount< 0:
            raise ValueError("Stock cannot be negative.")
        self.quantity-= amount
        self.save()
        return self.quantity

    def set_stock(self, amount: int):
        """
        Sets the stock quantity of the product.

        Ensures that stock quantity is non-negative.

        Args:
            amount: int value representing the new stock quantity.

        Returns:
            Updated stock quantity as an int.

        Raises:
            ValueError: If the given stock amount is negative.
        """
        if amount< 0:
            raise ValueError("Stock cannot be negative.")
        self.quantity= amount
        self.save()
        return amount

    def set_price(self, amount: int):
        """
        Updates the product price.

        Ensures that the price is non-negative.

        Args:
            amount: int value representing the new product price.

        Returns:
            Updated price as an int.

        Raises:
            ValueError: If the given price amount is negative.
        """
        if amount< 0:
            raise ValueError("Price cannot be negative.")
        self.price= amount
        self.save()
        return amount

    def modify_fields(self, data: dict):
        """
        Updates specified fields of the product.

        Ensures that only valid fields are updated.

        Args:
            data: dict containing fields to update and their new values.

        Returns:
            None.

        Raises:
            KeyError: If an invalid field is included in the update.
        """
        allowed_fields = {"name", "price", "brand", "quantity", "description"}
        for key, value in data.items():
            if key not in allowed_fields:
                raise KeyError(f"Field {key} is not a valid field.")
            setattr(self, key, value)
        self.save()

    def change_modified_timestamp(self):
        self.modified_at= datetime.datetime.utcnow()
        return

    def save(self, force_insert=False, validate=True, clean=True, write_concern=None, \
        cascade=None, cascade_kwargs=None, _refs=None, save_condition=None, \
        signal_kwargs=None, **kwargs):
        """
        Saves the product to the database, updating the modification timestamp.

        Args:
            Arguments for the `save` method of the parent 'Document' class from mongoengine.

        Returns:
            None.
        """
        self.change_modified_timestamp()
        super().save(force_insert=force_insert, validate=validate, clean=clean, \
            write_concern=write_concern, cascade=cascade, cascade_kwargs=cascade_kwargs, \
            _refs=_refs, save_condition=save_condition, signal_kwargs=signal_kwargs, **kwargs)

def create_product(data: dict)-> Product:
    """
    Creates a new product instance and saves it to the database.

    Ensures required fields are provided and assigns default values 
    to optional fields if missing.

    Args:
        data: dict instance containing product details. 
              Required keys: "name", "price", "quantity".
              Optional keys: "brand", "description".

    Returns:
        Created Product instance.
    """
    return Product(
        name=data["name"],
        price=data["price"],
        quantity=data["quantity"],
        brand=data.get("brand", ""),  # Default to an empty string
        description=data.get("description", "")  # Default to an empty string
    ).save()
