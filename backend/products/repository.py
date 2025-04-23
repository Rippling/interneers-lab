# repositories/product_repository.py

from products.models import Products,ProductCategory

class ProductRepository:
    
    @staticmethod
    def get_all_products():
        return Products.objects()

    @staticmethod
    def get_product_by_int_id(int_id):
        return Products.objects.get(int_id=int(int_id))

    @staticmethod
    def create_product(data):
        product = Products(**data)
        product.save()
        return product

    @staticmethod
    def update_product(product, data):
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete_product(product):
        product.delete()



class ProductCategoryRepository:
    
    @staticmethod
    def get_all_products():
        return ProductCategory.objects()

    @staticmethod
    def get_product_by_int_id(int_id):
        return ProductCategory.objects.get(_id=int(int_id))

    @staticmethod
    def create_product(data):
        product = ProductCategory(**data)
        product.save()
        return product

    @staticmethod
    def update_product(product, data):
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete_product(product):
        product.delete()
