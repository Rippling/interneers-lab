from bson import ObjectId
from ..repository import ProductRepository, CategoryRepository
from ..exceptions import *
from ..validators import *

class CategoryService:

    def __init__(self, category_repository=CategoryRepository()):
        self.category_repository = category_repository

    def create_category(self, data):
        return self.category_repository.create(data)

    def get_all_categories(self):
        return self.category_repository.get_all()

    def get_category(self, category_id):

        if not ObjectId.is_valid(category_id):
            raise InvalidCategoryId(category_id=category_id)

        category = self.category_repository.get_by_id(category_id)

        if not category:
            raise CategoryNotFound(category_id=category_id)

        return category

    def update_category(self, category_id, data, fields_required=True):

        category = self.get_category(category_id)

        for key, value in data.items():
            setattr(category, key, value)

        return self.category_repository.update(category)

    def delete_category(self, category_id):

        category = self.get_category(category_id)

        self.category_repository.delete(category_id)

        return category