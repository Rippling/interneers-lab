from .models import Product
from .test_connection import init_db
from datetime import datetime

init_db()  # Connect to MongoDB

class ProductRepository:
    @staticmethod
    def create(data):
        """Create a new product in the database."""
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def get_all(page=1, per_page=10):
        """Retrieve all products with pagination."""
        skip_count = (page - 1) * per_page  # Calculate offset
        products = Product.objects().order_by('-created_at').skip(skip_count).limit(per_page)
        return list(products)  # ✅ Return list of Product objects

    @staticmethod
    def get_by_id(product_id):
        """Retrieve a single product by ID."""
        return Product.objects(id=product_id).first()  # ✅ Return Product object

    @staticmethod
    def get_by_date_range(start_date, end_date):
        """Retrieve products created within a specific date range."""
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        products = Product.objects(created_at__gte=start_date, created_at__lte=end_date)
        return list(products)  # ✅ Return list of Product objects

    @staticmethod
    def update(product_id, update_data):
        """Update an existing product."""
        product = Product.objects(id=product_id).first()
        if product:
            for key, value in update_data.items():
                setattr(product, key, value)
            product.updated_at = datetime.utcnow()
            product.save()
            return product  # ✅ Return updated Product object
        return None

    @staticmethod
    def delete(product_id):
        """Delete a product from the database."""
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
            return True
        return False

    @staticmethod
    def format_product(product):
        """Format product data for API response."""
        return {
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": float(product.price),
            "brand": product.brand,
            "quantity_in_warehouse": product.quantity_in_warehouse,
            "created_at": product.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": product.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
