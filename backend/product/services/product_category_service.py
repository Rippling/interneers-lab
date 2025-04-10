from mongoengine.errors import NotUniqueError
from bson import ObjectId
from product.repositories.product_category_repository import ProductCategoryRepository

class ProductCategoryService:
    def __init__(self):
        self.repo = ProductCategoryRepository()

    def create_category(self, category_data):
        try:
            return self.repo.create_category(category_data)
        except NotUniqueError:
            raise ValueError("Category with this name already exists.")

    def get_all_categories(self):
        return self.repo.get_all_categories()

    def get_category_by_id(self, category_id):
        if not ObjectId.is_valid(category_id):
            return None
        return self.repo.get_category_by_id(category_id)

    def update_category(self, category_id, updated_data):
        category = self.get_category_by_id(category_id)
        if not category:
            return None
        return self.repo.update_category(category, updated_data)

    def delete_category(self, category_id):
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        return self.repo.delete_category(category)
