from product.models.category import ProductCategory
from product.models.product_model import Product
from bson import ObjectId

class ProductCategoryRepository:
    def create_category(self, category_data):
        category = ProductCategory(**category_data)
        category.save()
        return category

    def get_all_categories(self):
        return ProductCategory.objects.filter(is_active=True)

    def get_category_by_id(self, category_id):
        if not ObjectId.is_valid(category_id):
            return None
        return ProductCategory.objects(id=ObjectId(category_id)).first()

    def update_category(self, category_id, updated_data):
        category = self.get_category_by_id(category_id)
        if category:
            for key, value in updated_data.items():
                setattr(category, key, value)
            category.save()
            return category
        return None

    def delete_category(self, category_id):
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            return False

        # Removes this category from all products
        Product.objects(category=category).update(pull__category=category)

        # Then deletes the category
        category.delete()
        return True
