from product.models.category import ProductCategory
from product.models.product_model import Product
from mongoengine.errors import NotUniqueError
from bson import ObjectId

class ProductCategoryRepository:
    def create_category(self, category_data):
        try: 
            category = ProductCategory(**category_data)
            category.save()
            return category
        except NotUniqueError:
            raise

    def get_all_categories(self):
        return ProductCategory.objects.filter(is_active=True)

    def get_category_by_id(self, category_id):
        if not ObjectId.is_valid(category_id):
            return None
        return ProductCategory.objects(id=ObjectId(category_id)).first()

    def update_category(self, category, updated_data):
        for key, value in updated_data.items():
            setattr(category, key, value)
        category.save()
        return category

    def delete_category(self, category):
        Product.objects(category=category).update(pull__category=category)
        category.delete()
        return True
