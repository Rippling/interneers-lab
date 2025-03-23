from products.repositories.product_repository import ProductRepository
from mongoengine.errors import DoesNotExist, ValidationError

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
    
    def get_all_products(self):
        """
        Service method to get all products
        """
        return self.repository.get_all_products()
    
    def get_product_by_id(self, product_id):
        """
        Service method to get a product by ID
        """
        try:
            return self.repository.get_product_by_id(product_id)
        except DoesNotExist:
            raise ValueError(f"No product with id {product_id} exists.")
        except ValidationError:
            raise ValueError("Invalid ObjectId format")
    
    def create_product(self, product_data):
        """
        Service method to create a new product
        """
        return self.repository.create_product(product_data)
    
    def update_product(self, product_id, product_data):
        """
        Service method to update an existing product
        """
        try:
            product = self.repository.get_product_by_id(product_id)
            return self.repository.update_product(product, product_data)
        except DoesNotExist:
            raise ValueError(f"No product with id {product_id} exists.")
        except ValidationError:
            raise ValueError("Invalid ObjectId format")
    
    def delete_product(self, product_id):
        """
        Service method to delete a product
        """
        try:
            product = self.repository.get_product_by_id(product_id)
            self.repository.delete_product(product)
        except DoesNotExist:
            raise ValueError(f"No product with id {product_id} exists.")
        except ValidationError:
            raise ValueError("Invalid ObjectId format")
