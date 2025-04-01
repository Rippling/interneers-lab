from product.repositories.product_repository import ProductRepository
from product.models.category import ProductCategory
from product.models.product_model import Product
from mongoengine.queryset.visitor import Q
class ProductService:
    @staticmethod
    def create_product(data):
        required_fields = ["name", "category", "price_in_RS", "quantity", "manufacture_date", "expiry_date"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"{field} is required.")

        return ProductRepository.create_product(data)

    @staticmethod
    def get_filtered_products(category_name):
        """function to get products by category."""
        products, error = ProductRepository.get_products_by_category(category_name)
        if error:
            return None, error 
        return products, None

    @staticmethod
    def get_product_by_id(product_id):
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            return None, "Product not found."
        return product, None
    
    @staticmethod
    def get_all_products():
        return ProductRepository.get_all_products()

    @staticmethod
    def update_product(product_id, data):
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if "id" in data:
            raise ValueError("Updating the product ID is not allowed")
        updated_product = ProductRepository.update_product(product_id, data)
        return updated_product  
    
    @staticmethod
    def delete_product(product_id):
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found at service layer")
        return ProductRepository.delete_product(product_id)
    
    def add_category_to_product(product_id, category_id):
        return ProductRepository.add_category_to_product(product_id, category_id)

    @staticmethod
    def remove_category_from_product(product_id, category_id):
        return ProductRepository.remove_category_from_product(product_id, category_id)

