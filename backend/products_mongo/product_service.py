from .product_repository import ProductRepository

class ProductService:
    @staticmethod
    def create_product(data):
        return ProductRepository.create(data) 

    @staticmethod
    def get_product_by_id(product_id):
        """Retrieve a single product by ID and format it."""
        product = ProductRepository.get_by_id(product_id)
        return ProductRepository.format_product(product) if product else None  # ✅ Use format_product

    @staticmethod
    def get_all_products(page=1, per_page=10):
        """Retrieve all products with pagination and format them."""
        products = ProductRepository.get_all(page, per_page)
        return [ProductRepository.format_product(product) for product in products]  # ✅ Format list of products

    @staticmethod
    def update_product(product_id, data):
        """Update a product and return formatted data."""
        product = ProductRepository.update(product_id, data)
        return ProductRepository.format_product(product) if product else None  # ✅ Format updated product

    @staticmethod
    def delete_product(product_id):
        """Delete a product and return the status."""
        return ProductRepository.delete(product_id)  # ✅ No need to format

    @staticmethod
    def get_product_by_date_range(start_date, end_date):
        """Retrieve products by date range and format them."""
        products = ProductRepository.get_by_date_range(start_date, end_date)
        return [ProductRepository.format_product(product) for product in products]  # ✅ Format date-range products