# repositories/product_repository.py

from products.models import Products,ProductCategory

class ProductRepository:
    
    @staticmethod
    def get_all_products():
        return Products.objects.all()

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

    @staticmethod
    def filter_products_by_category(category):
        return Products.objects.filter(category=category)



class ProductCategoryRepository:
    
    @staticmethod
    def get_all_categories():
        return ProductCategory.objects.all()

    @staticmethod
    def get_category_by_id(int_id):
        return ProductCategory.objects.get(category_id=int(int_id))

    @staticmethod
    def create_category(data):
        category = ProductCategory(**data)
        category.save()
        return category

    @staticmethod
    def update_category(category, data):
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete_category(category):
        category.delete()



