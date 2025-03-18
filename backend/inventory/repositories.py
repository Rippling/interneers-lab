from .models import Product
from bson import ObjectId


class ProductRepository:

    @staticmethod
    def get_all_products():
        return Product.objects()

    @staticmethod
    def get_product_by_id(id):
        try:
            return Product.objects.get(id=ObjectId(id)) 
        except Product.DoesNotExist:
            return None

    @staticmethod
    def create_product(product_data):
        product = Product(
            name=product_data['name'],
            description=product_data['description'], 
            category=product_data['category'],
            price=product_data['price'], 
            brand=product_data['brand'],
            quantity=product_data['quantity']
        )
        product.save()
        return product

    @staticmethod
    def update_product(product, product_data):
        for key, value in product_data.items():
            if hasattr(product, key): 
                setattr(product, key, value)
        
        product.save()
        return product

    @staticmethod
    def delete_product(product):
        product.delete()
