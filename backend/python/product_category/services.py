from .repository import ProductCategoryRepository

class ProductCategoryService:
    @staticmethod
    def create_product_category(data):
        return ProductCategoryRepository.create(data)

    @staticmethod
    def get_all_product_categories():
        return ProductCategoryRepository.get_all()

    @staticmethod
    def get_product_category_by_id(product_category_id):
        product_category = ProductCategoryRepository.get_by_id(product_category_id)
        if not product_category:
            raise ValueError("Product Category not found")
        return product_category

    @staticmethod
    def update_product_category(product_category_id, data):
        product_category = ProductCategoryRepository.get_by_id(product_category_id)
        if not product_category:
            raise ValueError("Product Category not found")
        return ProductCategoryRepository.update(product_category_id, data)

    @staticmethod
    def delete_product_category(product_category_id):
        return ProductCategoryRepository.delete(product_category_id)