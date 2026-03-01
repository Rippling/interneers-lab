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
    def delete_product(product_id):
        return ProductRepository.delete_by_id(product_id)
