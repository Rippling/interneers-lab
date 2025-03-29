from .models import Product, ProductCategory
from bson import ObjectId


class ProductCategoryRepository:

    @staticmethod
    def create_category(data):
        """Create a new category or get existing one"""
        category = ProductCategory.objects(title=data["title"]).first()
        if not category:
            category = ProductCategory(**data)
            category.save()
        return category

    @staticmethod
    def get_category_by_id(category_id):
        """Fetch category by ID"""
        if not ObjectId.is_valid(category_id):
            return None
        return ProductCategory.objects(id=ObjectId(category_id)).first()

    @staticmethod
    def get_all_categories():
        """Fetch all categories"""
        return ProductCategory.objects()

    @staticmethod
    def update_category(category_id, data):
        """Update category by ID"""
        if not ObjectId.is_valid(category_id):
            return 0
        return ProductCategory.objects.filter(id=ObjectId(category_id)).update(**data)

    @staticmethod
    def delete_category(category_id):
        """Delete category by ID"""
        if not ObjectId.is_valid(category_id):
            return 0
        return ProductCategory.objects(id=ObjectId(category_id)).delete()


class ProductRepository:

    @staticmethod
    def create_product(data):
        """Create and save a product"""
        # Check for required fields
        if not data.get("brand"):
            raise ValueError("Brand is required")

        # Get or create category automatically
        category_data = {"title": data.get("category", "Uncategorized"), "description": ""}
        category = ProductCategoryRepository.create_category(category_data)

        # Create and save product
        product = Product(**data)
        product.set_category(category)
        product.save()
        return product

    @staticmethod
    def get_product_by_id(product_id):
        """Fetch product by ID"""
        if not ObjectId.is_valid(product_id):
            return None
        return Product.objects(id=ObjectId(product_id)).first()

    @staticmethod
    def get_all_products(fields=None, order_by=None):
        """Fetch all products with optional filtering and ordering"""

        # Base query
        query = Product.objects()

        # If specific fields are provided, include only those fields
        if fields:
            all_fields = {"name", "description", "category", "price", "brand", "quantity"}
            valid_fields = set(fields).intersection(all_fields)
            valid_fields.add("id")  # Always include 'id'
            query = query.only(*valid_fields)

        # Apply ordering if specified
        if order_by:
            query = query.order_by(order_by)

        return query


    @staticmethod
    def get_products_by_category(category_name, fields=None, order_by=None):
        """Get products belonging to a particular category with filters and ordering"""

        # Fetch category reference by title
        category_ref = ProductCategory.objects(title=category_name).first()

        if not category_ref:
            return []

        # Base query to get products by category
        query = Product.objects.filter(category__title=category_name)

        # If specific fields are provided, include only those fields
        if fields:
            all_fields = {"name", "description", "category", "price", "brand", "quantity"}
            valid_fields = set(fields).intersection(all_fields)
            valid_fields.add("id")  # Always include 'id'
            query = query.only(*valid_fields)

        # Apply ordering if specified
        if order_by:
            query = query.order_by(order_by)

        return query

    @staticmethod
    def update_product(product_id, data):
        """Update product by ID"""
        if not ObjectId.is_valid(product_id):
            return 0

        # Handle category update if necessary
        if "category" in data:
            category_data = {"title": data["category"], "description": ""}
            category = ProductCategoryRepository.create_category(category_data)
            product = Product.objects(id=ObjectId(product_id)).first()
            product.set_category(category)
            product.save()

        return Product.objects.filter(id=ObjectId(product_id)).update(**data)

    @staticmethod
    def delete_product(product_id):
        """Delete product by ID"""
        if not ObjectId.is_valid(product_id):
            return 0
        return Product.objects(id=ObjectId(product_id)).delete()
