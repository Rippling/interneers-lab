import mongoengine
from mongoengine import Document,fields     #mongodb ORM for django
from datetime import datetime,timezone
from .CategoryModel import ProductCategory

#This prod. model represent a prod. in db
class Product(Document):
    name=fields.StringField(required=True,max_length=200)
    description=fields.StringField()
    category=fields.ReferenceField(ProductCategory,reverse_delete_rule=mongoengine.PULL) #reference to the ProductCategory model
    price=fields.DecimalField(required=True,precision=2)
    brand=fields.StringField(required=True,min_length=1)
    quantity=fields.IntField(required=True)
    created_at=fields.DateTimeField(default=datetime.now(timezone.utc))
    updated_at=fields.DateTimeField(default=datetime.now(timezone.utc))
    
    meta = {
        'collection': 'products',
        'ordering': ['-created_at']         #use of created-at to sort by most recent prod.
    }

    def save(self, *args, **kwargs):
        #if prod. already exists store previous record in history
        if self.pk:  
            old_product=Product.objects(pk=self.pk).first()
            if old_product:
                ProductHistory.create_version(old_product)      #store old prod. before updating

        self.updated_at=datetime.now(timezone.utc)        #update updated_at timestamp
        
        if not self.created_at:
            self.created_at=datetime.now(timezone.utc)
       
       #brand validation that it should not be empty or contain whitespace
        if not self.brand or len(self.brand.strip()) == 0:   
            raise ValueError("Brand cannot be empty")
        return super(Product, self).save(*args, **kwargs)  
    
#this model stores the updates made in the prod.
class ProductHistory(Document):
    product_id=fields.StringField(required=True)
    name=fields.StringField(required=True, max_length=200)
    description=fields.StringField()
    category=fields.StringField()
    price=fields.DecimalField(required=True, precision=2)
    brand=fields.StringField(required=True)
    quantity=fields.IntField(required=True)
    updated_at=fields.DateTimeField()
    version_created_at=fields.DateTimeField(default=datetime.now(timezone.utc))     #prod. version creation timestamp

    meta = {'collection': 'product_history',
    'ordering': ['-version_created_at']         #sorting by most recent prod. version
    }

    # creates a new entry in prod. history model before updating main prod.
    @classmethod
    def create_version(cls, old_product):
        product_id=str(old_product.pk) if old_product.pk else None
        category_value=str(old_product.category.id) if old_product.category else None
        cls(
            product_id=product_id,
            name=old_product.name,
            description=old_product.description,
            category=category_value,
            price=old_product.price,
            brand=old_product.brand,
            quantity=old_product.quantity,
            updated_at=old_product.updated_at,
            version_created_at=datetime.now(timezone.utc)
        ).save()
