from ..models.ProductModel import Product
from ..repository.ProductCategoryRepo import ProductCategoryRepo

class CategoryService:
    def __init__(self):
        self.repository = ProductCategoryRepo()              #initialize ProductCategoryRepo instance

    #service methods which call corr. ProductCategoryRepo methods to perform diff. tasks

    def create_category(self, category_data):
        return self.repository.create(category_data)

    def get_all_categories(self):
        return self.repository.find_all()

    def get_category_by_id(self,category_id):
        return self.repository.find_by_id(category_id)

    def search_categories_by_title(self, title):
        return self.repository.search_by_title(title)

    def update_category(self, category_id, category_data):
        return self.repository.update(category_id, category_data)

    def delete_category(self, category_id):
        return self.repository.delete(category_id)

    def get_products_in_category(self, category_id):
        category=self.repository.find_by_id(category_id)
        if not category:
            return []
        return Product.objects.filter(category=category)
    
    def add_prod_to_category(self,category_id,product_id):
        return self.repository.add_prod_to_category(category_id,product_id)

    def remove_prod_from_category(self,product_id):
        return self.repository.remove_prod_from_category(product_id)