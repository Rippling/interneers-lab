from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from products.models import ProductCategory
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ProductCategoryDetail:
    title: str
    description: Optional[str] = None
    id: Optional[str] = (
        None  
    )

    @classmethod
    def from_product_category_model(cls, category_model):
        """Convert ProductCategory model to ProductCategoryDetail"""
        return cls(
            id=str(category_model.id) if category_model.id else None,
            title=category_model.title,
            description=category_model.description,
        )


class ProductCategoryRepository:
    def get_all(self):
        """Get all categories"""
        try:
            categories = ProductCategory.objects.all()
            return [
                ProductCategoryDetail.from_product_category_model(cat)
                for cat in categories
            ]
        except Exception as e:
            raise ValueError(f"An error occurred while fetching categories: {str(e)}")

    def get_by_id(self, category_id):
        """Get category by ID"""
        try:
            category = ProductCategory.objects.get(id=category_id)
            return ProductCategoryDetail.from_product_category_model(category)
        except DoesNotExist:
            raise ValueError(f"Category with id {category_id} not found")
        except ValidationError as e:
            raise ValueError(f"Invalid category ID: {str(e)}")

    def get_by_title(self, title):
        """Get category by title"""
        try:
            category = ProductCategory.objects(title=title).first()
            return (
                ProductCategoryDetail.from_product_category_model(category)
                if category
                else None
            )
        except ValidationError as e:
            raise ValueError(f"Invalid title: {str(e)}")

    def create(self, category_data):
        """Create new category"""
        try:
            category = ProductCategory(**asdict(category_data)).save()
            return ProductCategoryDetail.from_product_category_model(category)
        except NotUniqueError:
            raise ValueError("Category title must be unique")
        except ValidationError as e:
            raise ValueError(f"Validation error: {str(e)}")

    def update(self, category_id, category_data):
        """Update existing category"""
        try:
            category = ProductCategory.objects.get(id=category_id)

            update_data = asdict(category_data)

            update_data.pop("id", None)  # Remove id=None

            category.update(**update_data)
            category.reload()

            return ProductCategoryDetail.from_product_category_model(category)

        except NotUniqueError:
            raise ValueError("Category title must be unique")
        except ProductCategory.DoesNotExist:
            raise ValueError(f"Category with id {category_id} not found")


    def delete(self, category_id):
        """Delete category from mongo database"""
        try:
            
            category = ProductCategory.objects.get(id=category_id)
            category.delete()
            return True
        except DoesNotExist:
            raise ValueError(f"Category with id {category_id} not found.")
        except ValidationError as e:
            raise ValueError(f"Invalid category ID: {str(e)}")
