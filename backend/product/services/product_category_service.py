from product.models.category import ProductCategory
from product.repositories.product_category_repository import ProductCategoryRepository

class ProductCategoryService:
    @staticmethod
    def create_category(category_data):
        return ProductCategoryRepository.create_category(category_data)

    @staticmethod
    def get_all_categories():
        return ProductCategoryRepository.get_all_categories()

    @staticmethod
    def get_category_by_id(category_id):
        return ProductCategoryRepository.get_category_by_id(category_id)

    @staticmethod
    def update_category(category_id, updated_data):
        return ProductCategoryRepository.update_category(category_id, updated_data)

    @staticmethod
    def delete_category(category_id):
        return ProductCategoryRepository.delete_category(category_id)
