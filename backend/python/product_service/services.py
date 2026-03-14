from .repository import ProductRepository

class ProductServices():
    
    @staticmethod
    def create_product(data):
        if data.get("price", 0) <= 0:
            raise ValueError("Given Price is not valid")
        
        return ProductRepository.create(data)
    
    @staticmethod
    def list_products():
        return ProductRepository.get_all()
    
    @staticmethod
    def get_product(product_id):
        product = ProductRepository.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")
        
        return product
   
    @staticmethod
    def list_products_by_category_id(category_id):
        return ProductRepository.get_all_by_category_id(category_id)
    
    @staticmethod
    def remove_category_from_product(product_id):
        product = ProductRepository.remove_category_from_product(product_id)
        if not product:
            raise ValueError("Product not found")
        return product
    
    @staticmethod
    def add_category_to_product(product_id, category_id):
        product = ProductRepository.add_category_to_product(product_id, category_id)
        if not product:
            raise ValueError("Product not found")
        return product
    
    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete_by_id(product_id)
