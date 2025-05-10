# services/product_service.py

from products.repository import ProductRepository, ProductCategoryRepository

class ProductService:

    @staticmethod
    def list_products():
        return ProductRepository.get_all_products()

    @staticmethod
    def retrieve_product(int_id):
        return ProductRepository.get_product_by_int_id(int_id)

    @staticmethod
    def create_product(data):
        return ProductRepository.create_product(data)

    @staticmethod
    def update_product(int_id, data):
        product = ProductRepository.get_product_by_int_id(int_id)
        return ProductRepository.update_product(product, data)

    @staticmethod
    def delete_product(int_id):
        product = ProductRepository.get_product_by_int_id(int_id)
        ProductRepository.delete_product(product)
        return product
    
    
    



class ProductCategoryService:

    @staticmethod
    def list_categories():
        return ProductCategoryRepository.get_all_categories()

    @staticmethod
    def retrieve_category(category_id):
        return ProductCategoryRepository.get_category_by_id(category_id)

    @staticmethod
    def create_category(data):
        return ProductCategoryRepository.create_category(data)

    @staticmethod
    def update_category(category_id, data):
        category = ProductCategoryRepository.get_category_by_id(category_id)
        return ProductCategoryRepository.update_category(category, data)

    @staticmethod
    def delete_category(category_id):
        category = ProductCategoryRepository.get_category_by_id(category_id)
        ProductCategoryRepository.delete_category(category)
        return category
    
    @staticmethod
    def filter_products_by_category(category):
        return ProductRepository.filter_products_by_category(category)

    
    @staticmethod
    def delete_products_by_category(category):
        result = ProductRepository.filter_products_by_category(category=category).delete()
        return result.get("n", 0)  # returns number of deleted documents

