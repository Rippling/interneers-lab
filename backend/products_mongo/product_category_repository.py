from .models import ProductCategory

class ProductCategoryRepository:
    @staticmethod
    def create_category(data):
        """Create and return a new category."""
        category = ProductCategory(**data)
        category.save()
        return category

    @staticmethod
    def get_all_categories():
        """Retrieve all categories."""
        return list(ProductCategory.objects())

    @staticmethod
    def get_category_by_id(category_id):
        """Retrieve a single category by its ID."""
        return ProductCategory.objects(id=category_id).first()

    @staticmethod
    def update_category(category_id, update_data):
        """Update a category by ID."""
        category = ProductCategory.objects(id=category_id).first()
        if category:
            category.update(**update_data)
            return ProductCategory.objects(id=category_id).first()  # Return updated category
        return None

    @staticmethod
    def delete_category(category_id):
        """Delete a category by ID."""
        category = ProductCategory.objects(id=category_id).first()
        if category:
            category.delete()
            return True
        return False

    @staticmethod
    def format_category(category):
        """Ensure the category is formatted correctly before returning."""
        if isinstance(category, dict):
        # If category is already a dictionary, return it directly
          return category

        return {
            "id": str(category.id),  # Convert ObjectId to string
            "title": category.title,
            "description": category.description,
        } 

