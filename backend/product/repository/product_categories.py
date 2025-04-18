from product.models.product_category import ProductCategory
from product.models.product import Product

class ProductCategoryRepository:
    def create_category(self, data):
        category = ProductCategory(**data)
        category.save()
        return category
    
    def get_category(self, category_id):
        return ProductCategory.objects(id=category_id).first()
    
    def get_all_categories(self):
        return ProductCategory.objects.all()
    
    def update_category(self, category_id, data):
        category = self.get_category(category_id)
        if category:
            for key, value in data.items():
                setattr(category, key, value)
            category.save()
        return category
    
    def delete_category(self, category_id):
        print(category_id)
        category = self.get_category(category_id)
        print(category)
        if category:
            category.delete()
        return category
    
    def list_product_in_category(self, category_id):
        return Product.objects(category=category_id)