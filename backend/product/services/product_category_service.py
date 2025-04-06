from product.models.category import ProductCategory
from product.repositories.product_category_repository import ProductCategoryRepository

class ProductCategoryService:
    def __init__(self):
        self.product_category_repository = ProductCategoryRepository()
        
    def create_category(self, category_data):
        return self.product_category_repository.create_category(category_data)

    def get_all_categories(self):
        return self.product_category_repository.get_all_categories()

    def get_category_by_id(self, category_id):
        return self.product_category_repository.get_category_by_id(category_id)

    def update_category(self, category_id, updated_data):
        return self.product_category_repository.update_category(category_id, updated_data)

    def delete_category(self, category_id):
        return self.product_category_repository.delete_category(category_id)
