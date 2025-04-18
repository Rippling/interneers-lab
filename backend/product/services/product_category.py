from product.repository.product_categories import ProductCategoryRepository
from product.services.product import ProductService


class ProductCategoryService:
    def __init__(self):
        self.repo = ProductCategoryRepository()
        self.product_service = ProductService()

    def create_category(self, data):
        return self.repo.create_category(data)
    
    def get_category(self, category_id):
        category = self.repo.get_category(category_id)
        if not category:
            raise ValueError("Category not found.")
        return category
    
    def update_category(self, category_id, data):
        category = self.repo.get_category(category_id)
        if not category:
            raise ValueError("Category not found.")
        return self.repo.update_category(category_id, data)
    
    def delete_category(self, category_id):
        category = self.repo.get_category(category_id)
        if not category:
            raise ValueError("Category not found.")
        return self.repo.delete_category(category_id)
    
    def get_all_category(self):
        return self.repo.get_all_categories()
    
    def list_products_in_category(self, category_id):
        return self.repo.list_product_in_category(category_id)

    def add_product_to_category(self, category_id, product_id):
        category = self.get_category(category_id)
        product = self.product_service.get_product(product_id)
        if not product:
            raise ValueError("Product not found.")
        return self.product_service.update_product(product_id, {"category": category})
    
    def remove_product_from_category(self, category_id, product_id):
        product = self.product_service.get_product(product_id)
        if not product:
            raise ValueError("Product not found.")
        if product.category and str(product.category.id) == str(category_id):
            return self.product_service.update_product(product_id, {"category": None})
        return product