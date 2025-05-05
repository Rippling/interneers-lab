from .models import Product, Category
from mongoengine.errors import DoesNotExist

class CategoryRepository:
    @staticmethod
    def get_by_slug(slug):
        try:
            return Category.objects.get(slug=slug)
        except DoesNotExist:
            return None

    @staticmethod
    def get_by_id(id):
        try:
            return Category.objects.get(id=id)
        except DoesNotExist:
            return None

    @staticmethod
    def list_all():
        return list(Category.objects.all())

    @staticmethod
    def create(data):
        category = Category(**data)
        category.save()
        return category

    @staticmethod
    def delete(category):
        category.delete()

class ProductRepository:
    @staticmethod
    def get_by_slug(slug):
        try:
            return Product.objects.get(slug=slug)
        except DoesNotExist:
            return None

    @staticmethod
    def get_by_id(id):
        try:
            return Product.objects.get(id=id)
        except DoesNotExist:
            return None

    @staticmethod
    def list_all(filters=None):
        qs = Product.objects
        if filters:
            qs = qs.filter(**filters)
        return list(qs)

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update(product, data):
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete(product):
        product.delete() 