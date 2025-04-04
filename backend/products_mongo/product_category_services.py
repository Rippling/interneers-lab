from .product_category_repository import ProductCategoryRepository
from .models import ProductCategory, Product

class ProductCategoryService:
    @staticmethod
    def create_category(data):
        """Create a new product category."""
        category = ProductCategoryRepository.create_category(data)
        return ProductCategoryRepository.format_category(category)

    @staticmethod
    def get_all_categories():
        """Retrieve all product categories."""
        categories = ProductCategoryRepository.get_all_categories()
        return [ProductCategoryRepository.format_category(cat) for cat in categories]

    @staticmethod
    def get_category_by_id(category_id):
        """Retrieve a single category by ID."""
        category = ProductCategoryRepository.get_category_by_id(category_id)
        return ProductCategoryRepository.format_category(category) if category else None

    @staticmethod
    def update_category(category_id, update_data):
        """Update an existing category."""
        updated_category = ProductCategoryRepository.update_category(category_id, update_data)
        return ProductCategoryRepository.format_category(updated_category) if updated_category else None

    @staticmethod
    def delete_category(category_id):
        """Delete a category from the database."""
        return ProductCategoryRepository.delete_category(category_id)
    
    @staticmethod
    def get_products_by_category(category_id):
        """Retrieve all products under a specific category."""
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            return None  # Category not found

        products = Product.objects(category=category)  # Fetch all products in this category
        return {
            "category": {
                "id": str(category.id),
                "title": category.title,
                "description": category.description,
                "products": [
                    {
                        "id": str(product.id),
                        "name": product.name,
                        "description": product.description,
                        "price": float(product.price),
                        "brand": product.brand,
                        "quantity_in_warehouse": product.quantity_in_warehouse
                    }
                    for product in products
                ]
            }
        }