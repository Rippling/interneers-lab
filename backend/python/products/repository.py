from bson import ObjectId
from .models import Product, Category


class ProductRepository:

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def get_all(sort_by):
        allowed_sorts = ['name', '-name', 'price', '-price', 'created_at', '-created_at', 'updated_at', '-updated_at']
        
        if sort_by not in allowed_sorts:
            sort_by = '-updated_at'
        return Product.objects().order_by(sort_by)

    @staticmethod
    def get_by_id(id):
        return Product.objects(id=id).first()

    @staticmethod
    def update(product):
        product.save()
        return product

    @staticmethod
    def delete(id):
        product = Product.objects(id=id).first()
        if product:
            product.delete()
        return product

    @staticmethod
    def get_all_by_category_id(category_id, sort_by):
        allowed_sorts = ['name', '-name', 'price', '-price', 'created_at', '-created_at', 'updated_at', '-updated_at']
        
        if sort_by not in allowed_sorts:
            sort_by = '-updated_at'
        return Product.objects(category=category_id).order_by(sort_by)


class CategoryRepository:

    @staticmethod
    def create(data):
        category = Category(**data)
        category.save()
        return category

    @staticmethod
    def get_all():
        return Category.objects()

    @staticmethod
    def get_by_id(category_id,):
        return Category.objects(id=category_id).first()

    @staticmethod
    def update(category):
        category.save()
        return category

    @staticmethod
    def delete(category_id):
        category = Category.objects(id=category_id).first()
        if category:
            category.delete()
        return category