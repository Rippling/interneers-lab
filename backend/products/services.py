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
    def list_products():
        return ProductCategoryRepository.get_all_products()

    @staticmethod
    def retrieve_product(category_id):
        return ProductCategoryRepository.get_product_by_int_id(category_id)

    @staticmethod
    def create_product(data):
        return ProductCategoryRepository.create_product(data)

    @staticmethod
    def update_product(int_id, data):
        product = ProductCategoryRepository.get_product_by_int_id(int_id)
        return ProductCategoryRepository.update_product(product, data)

    @staticmethod
    def delete_product(int_id):
        product = ProductCategoryRepository.get_product_by_int_id(int_id)
        ProductCategoryRepository.delete_product(product)
        return product
