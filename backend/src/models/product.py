import datetime
from mongoengine import Document, StringField, IntField, DateTimeField

class Product(Document):
    name= StringField(required= True)
    price= IntField(required= True)
    quantity= IntField(required= True)
    description= StringField(max_length= 250)

    created_at= DateTimeField(default= datetime.datetime.utcnow())
    modified_at= DateTimeField(default= datetime.datetime.utcnow())

    def modify_stock(self, amount: int):
        assert self.quantity > -amount
        self.quantity-= amount
        self.save()
        return self.quantity

    def set_stock(self, amount: int):
        assert amount >= 0
        self.quantity= amount
        self.save()
        return amount

    def set_price(self, amount: int):
        assert amount >= 0
        self.price= amount
        self.save()
        return amount

    def change_modified_timestamp(self):
        self.modified_at= datetime.datetime.utcnow()
        return
