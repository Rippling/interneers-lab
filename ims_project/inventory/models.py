from mongoengine import Document, StringField, IntField, DecimalField, QuerySet, DateTimeField
import datetime

class ProductQuerySet(QuerySet):
    
    def create_product(self, data):

        product = self._document(**data)
        product.save()
        return product
    
    def product_fetch(self, id):
        try:
            return self.get(id=id)
        except (self._document.DoesNotExist, Exception):
            return None 
            
    def fetch_all(self):
        return self.all()
    
    def delete_product(self, id):
        try:
            product = self.get(id=id)
            product.delete()
            return True
        except self._document.DoesNotExist:
            return False 


class ProductCategoryQuerySet(QuerySet):

    def create_product_category(self, data):

        product_category = self._document(**data)
        product_category.save()
        return product_category
    
    def product_category_fetch(self, title):
        try:
            return self.get(title=title)
        except (self._document.DoesNotExist, Exception):
            return None 

    def fetch_products(self, title):
        products_list = Product.objects(product_category=title)
        if products_list:
            return products_list
        return None

    def fetch_all(self):
        return self.all()
    
    def delete_product_category(self, title):
        try:
            product_category = self.get(title=title)
            product_category.delete()
            return True
        except self._document.DoesNotExist:
            return False 


class ProductCategory(Document):
    def __str__(self):
        return self.title
    
    title = StringField(required=True, max_length=200)
    description = StringField(max_length=400)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'queryset_class': ProductCategoryQuerySet, "collection": "product_categories"}

    def update_fields(self, data):
        # Accepts the dictionary directly
        self.updated_at = datetime.datetime.utcnow()
        for field, value in data.items():
            if hasattr(self, field):
                setattr(self, field, value)

        self.save()
        return self


class Product(Document):
    def __str__(self):
        return self.name

    name = StringField(required=True, max_length=200)
    description = StringField(required=True, max_length=500)
    brand = StringField(required=True, max_length=200)
    price = DecimalField(min_value=0, precision=2)
    quantity = IntField(min_value=0)
    product_category = StringField(max_length=200, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'products', 'queryset_class': ProductQuerySet}

    def update_fields(self, data):

        self.updated_at = datetime.datetime.utcnow()
        for field, value in data.items():
            if hasattr(self, field):
                setattr(self, field, value)

        self.save()
        return self