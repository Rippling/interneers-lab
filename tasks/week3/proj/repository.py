from .models import Product, ProductCategory
import json

class CategoryRepository:
    def create(self, data):
        category = ProductCategory(**data)
        category.save()
        return str(category.id)

    def get_all(self):
        return json.loads(ProductCategory.objects.all().to_json())
    
    def delete(self, category_id):
        category = ProductCategory.objects(id=category_id).first()
        if category:
            category.delete()
            return True
        return False

class ProductRepository:
    def get_by_category(self, category_id):
        # Fetch all products where the reference matches the category_id
        products = Product.objects(category=category_id)
        return json.loads(products.to_json())

    def update_category(self, product_id, category_id):
        product = Product.objects(id=product_id).first()
        if product:
            # Set the reference to the new category, or None to remove it
            product.category = category_id 
            product.save()
            return True
        return False

    def bulk_insert(self, product_objects):
        # MongoEngine's way to do a single, fast bulk insert
        Product.objects.insert(product_objects)