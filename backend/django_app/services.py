from .repository import ProductRepository, ProductCategoryRepository
from .models import Product, ProductCategory

class ProductCategoryService:

    @staticmethod
    def create_category(data):
        return ProductCategoryRepository.create_category(data)

    @staticmethod
    def get_category(category_id):
        category = ProductCategoryRepository.get_category_by_id(category_id)
        return category.to_dict() if category else None

    @staticmethod
    def list_categories():
        categories = ProductCategoryRepository.get_all_categories()
        return [category.to_dict() for category in categories]

    @staticmethod
    def update_category(category_id, data):
        return ProductCategoryRepository.update_category(category_id, data)

    @staticmethod
    def delete_category(category_id):
        return ProductCategoryRepository.delete_category(category_id)


class ProductService:

    @staticmethod
    def create_product(data):
        return ProductRepository.create_product(data).to_dict()

    @staticmethod
    def get_product(product_id):
        product = ProductRepository.get_product_by_id(product_id)
        return product.to_dict() if product else None

    @staticmethod
    def list_products(fields=None, order_by=None):
        """Fetch all products with optional filters and ordering"""
        products = ProductRepository.get_all_products(fields=fields, order_by=order_by)
        # Pass fields to to_dict()
        return [product.to_dict(fields) for product in products]


    @staticmethod
    def get_products_by_category(category_name, fields=None, order_by=None):
        """Fetch products by category with filters and ordering"""
        products = ProductRepository.get_products_by_category(category_name, fields=fields, order_by=order_by)
        # Pass fields to to_dict()
        return [product.to_dict(fields) for product in products]



    @staticmethod
    def update_product(product_id, data):
        return ProductRepository.update_product(product_id, data)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete_product(product_id)
