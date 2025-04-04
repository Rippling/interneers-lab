from .product_repository import ProductRepository
from .product_category_repository import ProductCategoryRepository
from .models import Product, ProductCategory
from bson import ObjectId
from bson.errors import InvalidId

class ProductService:
    @staticmethod
    def create_product(data):
        return ProductRepository.create(data)

    @staticmethod
    def get_product_by_id(product_id):
        """Retrieve a single product by ID and format it."""
        product = ProductRepository.get_by_id(product_id)
        return ProductRepository.format_product(product) if product else None

    @staticmethod
    def get_all_products(page=1, per_page=10):
        """Retrieve all products with pagination and format them."""
        products = ProductRepository.get_all(page, per_page)
        return [ProductRepository.format_product(product) for product in products]

    @staticmethod
    def update_product(product_id, data):
        """Update a product and return formatted data."""
        product = ProductRepository.update(product_id, data)
        return ProductRepository.format_product(product) if product else None

    @staticmethod
    def delete_product(product_id):
        """Delete a product and return the status."""
        return ProductRepository.delete(product_id)

    @staticmethod
    def get_product_by_date_range(start_date, end_date):
        """Retrieve products by date range and format them."""
        products = ProductRepository.get_by_date_range(start_date, end_date)
        return [ProductRepository.format_product(product) for product in products]
    
    @staticmethod
    def get_products_by_category(category_id, page=1, per_page=10):
        """Retrieve products by category with pagination."""
        try:
            category_obj_id = ObjectId(category_id)
        except Exception:
            return []
        category = ProductCategory.objects(id=category_obj_id).first()
        if not category:
            return []
        products = Product.objects.filter(category=category_obj_id).skip((page - 1) * per_page).limit(per_page)
        return list(products)
    

    @staticmethod
    def add_product_to_category(product_id, category_id):
        """Assign a product to a category."""
        product = ProductRepository.get_by_id(product_id)
        category = ProductCategoryRepository.get_category_by_id(category_id)

        if not product or not category:
            return None  # Product or category does not exist

        product.category = category  # Assuming a ForeignKey relationship in your model
        product.save()
        return product

    @staticmethod
    def remove_product_from_category(product_id):
        """Remove a product from its assigned category."""
        product = ProductRepository.get_by_id(product_id)
        
        if not product:
            return None  # Product does not exist

        product.category = None  # Unassign the category
        product.save()
        return product

    @staticmethod
    def get_filtered_products(category_id=None, name=None, min_price=None, max_price=None, brand=None, page=1, per_page=10):
        filters = {}

        if category_id:
            try:
                print('trying')
                print(category_id)
                print(filters)
                filters["category"] = ObjectId(category_id)  # Convert to ObjectId
            except InvalidId:
                return {"error": "Invalid category_id format"}
        if name:
            filters["name__icontains"] = name  # Case-insensitive search
        if min_price:
            filters["price__gte"] = min_price
        if max_price:
            filters["price__lte"] = max_price
        if brand:
            filters["brand__icontains"] = brand  # Case-insensitive search

    # Query the database
        products = Product.objects.filter(**filters)

    # Apply pagination
        start = (page - 1) * per_page
        end = start + per_page
        return products[start:end]



    
