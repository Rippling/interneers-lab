from .models import Product
from datetime import datetime
class ProductRepository:
    @staticmethod
    def get_all():
        return Product.objects.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def update(product, data):
        for key, value in data.items():
            setattr(product, key, value)
        product.updated_at = datetime.utcnow()
        product.save()
        return product

    @staticmethod
    def delete(product):
        product.delete()