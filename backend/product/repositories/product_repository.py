from product.models.product_model import Product
from product.models.category import ProductCategory
from datetime import datetime
from mongoengine.errors import DoesNotExist
import pytz

class ProductRepository:
    def create_product(self, data):
        data["created_at"] = datetime.now(pytz.utc)
        data["updated_at"] = datetime.now(pytz.utc)
        product = Product(**data)
        product.save()
        return product

    def get_all_products(self):
        return list(Product.objects())

    def get_products_by_category(self, category_name):
        category = ProductCategory.objects(category_name=category_name).first()
        if not category:
            return None, "Category does not exist."

        products = Product.objects(self, category=category)
        if not products:
            return [], f"No products found in category '{category_name}'."
        
        return products, None

    def get_product_by_id(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except DoesNotExist:
            return None

    def update_product(self, product_id, product_data):
        product = Product.objects(id=product_id).first()
        if not product:
            return None

        for key, value in product_data.items():
            setattr(product, key, value) 
        product.save()
        return product

    def delete_product(self, product_id):
        product = Product.objects(id=product_id).first()
        if product:
            product.delete()
            return True
        return False

    def add_category_to_product(self, product_id, category_id):
        """Add a category to an existing product."""
        product = Product.objects(id=product_id).first()
        category = ProductCategory.objects(id=category_id).first()

        if not product:
            return None, "Product not found"
        if not category:
            return None, "Category not found"

        if category not in product.category:
            product.category.append(category)
            product.save()

        return product, None
    
    def remove_category_from_product(self, product_id, category_id):
        """Remove a category from an existing product."""
        product = Product.objects(id=product_id).first()
        category = ProductCategory.objects(id=category_id).first()

        if not product:
            return None, "Product not found"
        if not category:
            return None, "Category not found"

        if category in product.category:
            product.category.remove(category)
            product.save()

        return product, None
