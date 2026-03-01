from .models import Product

class ProductRepository:

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product
    
    @staticmethod
    def get_all():
        return Product.objects()
    
    @staticmethod
    def get_by_id(product_id):
        return Product.objects(id=product_id).first()
    
    @staticmethod
    def delete_by_id(product_id):
        Product.objects(id=product_id).delete()