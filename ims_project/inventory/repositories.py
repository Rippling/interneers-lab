from .models import Product, ProductCategory

class ProductRepository:

    def get_by_id(self, product_id):
        return Product.objects.product_fetch(id=product_id)

    def get_all(self):
        return Product.objects.fetch_all()

    def add(self, data):
        try:
            return Product.objects.create_product(data)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Repository Error: {str(e)}")

    def update(self, instance, data):        
        return instance.update_fields(data)

    def remove(self, product_id):
        return Product.objects.delete_product(id=product_id)
    

class ProductCategoryRepository:

    def get_by_title(self, title):
        return ProductCategory.objects.product_category_fetch(title=title)

    def get_all(self):
        return ProductCategory.objects.fetch_all()

    def add(self, data):
        try:

            return ProductCategory.objects.create_product_category(data)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Repository Error: {str(e)}")

    def update(self, instance, data):
        return instance.update_fields(data)

    def remove(self, title):
        return ProductCategory.objects.delete_product_category(title=title)
    
    def fetch_products(self, title):
        return ProductCategory.objects.fetch_products(title)