from .models import Product, ProductCategory
from .test_connection import init_db
from datetime import datetime
from bson import DBRef, ObjectId

init_db()  # Connect to MongoDB

class ProductRepository:
    @staticmethod
    def create(data):
        """Create a new product in the database."""
        category_id = data.pop("category", None)
        if category_id:
            category = ProductCategory.objects(id=category_id).first()
            if category:
                data["category"] = category
            else:
                raise ValueError("Invalid Category ID")
            
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
            category_id = update_data.pop("category", None)
            if category_id:
                category = ProductCategory.objects(id=category_id).first()
                if category:
                    update_data["category"] = category
                else:
                    raise ValueError("Invalid category ID")
            
            for key, value in update_data.items():
                setattr(product, key, value)
            product.updated_at = datetime.utcnow()
            product.save()
            return product
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
    def update_product_category(product_id, category_id):
        """Update the category of a product"""
        product = Product.objects(id=product_id).first()
        category = ProductCategory.objects(id=category_id).first()

        if not product or not category:
            return None  # Either product or category doesn't exist
    
        product.category = category
        product.save()
        return product


    @staticmethod
    def format_product(product):
        if isinstance(product, dict):
            product_id = product.get("_id")
            category = product.get("category")
            created_at = product.get("created_at")
            updated_at = product.get("updated_at")

            if isinstance(category, DBRef):  
                category_doc = ProductCategory.objects(id=category.id).first()
                category = {"id": str(category_doc.id), "title": category_doc.title} if category_doc else None
            elif isinstance(category, ObjectId):  
                category_doc = ProductCategory.objects(id=category).first()
                category = {"id": str(category_doc.id), "title": category_doc.title} if category_doc else None
            elif isinstance(category, str):
                try:
                    category_doc = ProductCategory.objects(id=ObjectId(category)).first()
                    category = {"id": str(category_doc.id), "title": category_doc.title} if category_doc else None
                except:
                    category = None

        else:
            product_id = str(product.id)
            category = {
            "id": str(product.category.id),
            "title": product.category.title
            } if product.category else None
            created_at = product.created_at
            updated_at = product.updated_at
        def format_datetime(value):
            if isinstance(value, str):
                return value
            elif isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return None

        return {
        "id": str(product_id),
        "name": product["name"] if isinstance(product, dict) else product.name,
        "description": product["description"] if isinstance(product, dict) else product.description,
        "category": category,  # ✅ FIXED: Category now resolves correctly
        "price": float(product["price"]) if isinstance(product, dict) else float(product.price),
        "brand": product["brand"] if isinstance(product, dict) else product.brand,
        "quantity_in_warehouse": product["quantity_in_warehouse"] if isinstance(product, dict) else product.quantity_in_warehouse,
        "created_at": format_datetime(created_at),
        "updated_at": format_datetime(updated_at),
    }
