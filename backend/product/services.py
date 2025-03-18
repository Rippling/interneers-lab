from .repository import ProductRepository

class ProductService:
    @staticmethod
    def create_product(data):
        """Handles business logic before creating a product."""
        required_fields = ["name", "category", "price_in_RS", "quantity", "manufacture_date", "expiry_date"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"{field} is required.")

        return ProductRepository.create_product(data)

    @staticmethod
    def get_product_by_id(product_id):
        """Fetch a product by ID. Raises an error if not found."""
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return product

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


