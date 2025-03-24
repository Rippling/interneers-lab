import mongoengine
import datetime

class ProductCategory(mongoengine.Document):
    title = mongoengine.StringField(max_length=100, required=True, unique=True)
    description = mongoengine.StringField(required=False)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'ProductCategory'}  

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.utcnow()
        return super(ProductCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

