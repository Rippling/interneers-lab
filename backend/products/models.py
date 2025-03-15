import mongoengine
import datetime
class Product(mongoengine.Document):
    name = mongoengine.StringField(max_length=255, required=True)
    description = mongoengine.StringField(required=False)
    brand = mongoengine.StringField(max_length=100, required=False)
    category = mongoengine.StringField(max_length=100, required=True)
    price = mongoengine.DecimalField(precision=2, required=True)
    quantity = mongoengine.IntField(default=0, min_value=0)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    meta = {'collection': 'Product'}  

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
