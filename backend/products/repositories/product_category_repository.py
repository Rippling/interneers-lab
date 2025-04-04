from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from ..models import ProductCategory


class ProductCategoryRepository:
    def get_all(self):
        """Get all categories"""
        return ProductCategory.objects.all()

    def get_by_id(self, category_id):
        """Get category by ID"""
        try:
            return ProductCategory.objects.get(id=category_id)
        except (DoesNotExist, ValidationError):
            raise ValueError(f"Category with id {category_id} not found")

    def get_by_title(self, title):
        """Get category by title"""
        return ProductCategory.objects(title=title).first()

    def create(self, category_data):
        """Create new category"""
        try:
            return ProductCategory(**category_data).save()
        except NotUniqueError:
            raise ValueError("Category title must be unique")
        except ValidationError as e:
            raise ValueError(f"Validation error: {str(e)}")

    def update(self, category_id, category_data):
        """Update existing category"""
        try:
            category = self.get_by_id(category_id)
            category.update(**category_data)
            return category.reload()
        except NotUniqueError:
            raise ValueError("Category title must be unique")

    def delete(self, category_id):
        """Delete category"""
        category = self.get_by_id(category_id)
        category.delete()
