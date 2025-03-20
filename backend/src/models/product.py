import datetime
from mongoengine import Document, StringField, IntField, DateTimeField

class Product(Document):
    name= StringField(required= True)
    price= IntField(required= True)
    brand= StringField()
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

    def modify_fields(self, data: dict):
        for key in data.keys():
            if key=="name":
                self.name= data[key]
            elif key=="price":
                self.price= data[key]
            elif key=="brand":
                self.brand= data[key]
            elif key=="quantity":
                self.quantity= data[key]
            elif key=="description":
                self.description= data[key]
            else:
                raise KeyError(f"Field {key} is not a valid field.")
        self.change_modified_timestamp()
        self.save()

    def change_modified_timestamp(self):
        self.modified_at= datetime.datetime.utcnow()
        return

    def save(self, force_insert=False, validate=True, clean=True, write_concern=None, \
        cascade=None, cascade_kwargs=None, _refs=None, save_condition=None, \
        signal_kwargs=None, **kwargs):
        self.change_modified_timestamp()
        super().save(force_insert=force_insert, validate=validate, clean=clean, \
            write_concern=write_concern, cascade=cascade, cascade_kwargs=cascade_kwargs, \
            _refs=_refs, save_condition=save_condition, signal_kwargs=signal_kwargs, **kwargs)

def create_product(data: dict)-> Product:
    return Product(name= data["name"], price= data["price"], quantity= data["quantity"], \
        description= data["description"])