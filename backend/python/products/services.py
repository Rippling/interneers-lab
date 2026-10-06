from .repository import product_repo,category_repo

class ProductService:
    
    def get_all_products(self, filters = None):
        return product_repo.get_all_products(filters)

    def get_product_by_id(self, product_id):
        return product_repo.get_product_by_id(product_id)

    def create_product(self, product_data):
        if 'name' in product_data:
            product_data['name'] = product_data['name'].title()
        return product_repo.create_product(product_data)

    def delete_product(self, product_id):
        return product_repo.delete_product(product_id)
    
    def get_products_by_category(self, category_id):
        category = category_repo.get_category_by_id(category_id)
        if not category:
            return None 
        return product_repo.get_products_by_category(category_id)
    
    def update_product(self, product_id, update_data):
        if 'category' in update_data and update_data['category'] is not None:
            category_exists = category_repo.get_category_by_id(update_data['category'])
            
            if not category_exists:
                return {"error": "The provided category ID does not exist."}
        return product_repo.update_product(product_id=product_id,update_data=update_data)
    
    def bulk_create_products(self, product_list):
        return product_repo.bulk_create_products(product_data_list=product_list)

product_service = ProductService()

class ProductCategoryService:
    
    def get_all_categories(self):
        return category_repo.get_all_categories()

    def get_category_by_id(self, category_id):
        return category_repo.get_category_by_id(category_id)

    def create_category(self, category_data):
        if 'title' in category_data:
            category_data['title'] = category_data['title'].strip().title()
            
        return category_repo.create_category(category_data)

    def delete_category(self, category_id):
        return category_repo.delete_category(category_id)

category_service = ProductCategoryService()