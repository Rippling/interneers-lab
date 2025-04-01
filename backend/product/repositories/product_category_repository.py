from product.models.category import ProductCategory
from product.models.product_model import Product
from bson import ObjectId

class ProductCategoryRepository:
    @staticmethod
    def create_category(category_data):
        category = ProductCategory(**category_data)
        category.save()
        return category

    @staticmethod
    def get_all_categories():
        return ProductCategory.objects.filter(is_active=True)

    @staticmethod
    def get_category_by_id(category_id):
        if not ObjectId.is_valid(category_id):
            return None
        return ProductCategory.objects(id=ObjectId(category_id)).first()

    @staticmethod
    def update_category(category_id, updated_data):
        category = ProductCategoryRepository.get_category_by_id(category_id)
        if category:
            for key, value in updated_data.items():
                setattr(category, key, value)
            category.save()
            return category
        return None

    @staticmethod
    def delete_category(category_id):
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            return False

        # Removes this category from all products
        Product.objects(category=category).update(pull__category=category)

        # then deletes the category
        category.delete()
        return True
