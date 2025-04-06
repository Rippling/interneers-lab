from product.repositories.product_repository import ProductRepository
from mongoengine.queryset.visitor import Q

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()
        
    def create_product(self, data):
        required_fields = ["name", "brand", "category", "price_in_RS", "quantity", "manufacture_date", "expiry_date"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"{field} is required.")

        return self.product_repository.create_product(data)

    def get_filtered_products(self, category_name):
        """function to get products by category."""
        products, error = self.product_repository.get_products_by_category(category_name)
        if error:
            return None, error 
        return products, None

    def get_product_by_id(self, product_id):
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            return None, "Product not found."
        return product, None
    
    def get_all_products(self):
        return self.product_repository.get_all_products()

    def update_product(self, product_id, data):
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        if "id" in data:
            raise ValueError("Updating the product ID is not allowed")
        updated_product = self.product_repository.update_product(product_id, data)
        return updated_product  
    
    def delete_product(self, product_id):
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found at service layer")
        return self.product_repository.delete_product(product_id)
    
    def add_category_to_product(self, product_id, category_id):
        return self.product_repository.add_category_to_product(product_id, category_id)

    def remove_category_from_product(self, product_id, category_id):
        return self.product_repository.remove_category_from_product(product_id, category_id)

