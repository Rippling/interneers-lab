from .repositories import ProductRepository, ProductCategoryRepository
from .serializers import ProductSerializer, ProductCategorySerializer

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    def create_new_product(self, product_data):
        product_serializer = ProductSerializer(data=product_data)

        if product_serializer.is_valid():
            return product_serializer.save()

        raise ValueError(product_serializer.errors)

    def update_existing_product(self, product_id, update_data):

        old_product = self.product_repository.get_by_id(product_id=product_id)

        if not old_product:
            raise ValueError(f"Product {product_id} not found.")
        
        product_serializer = ProductSerializer(old_product, data=update_data, partial=True)
        
        if product_serializer.is_valid():
            return product_serializer.save()

        raise ValueError(product_serializer.errors)

    def get_all_products(self):
        return self.product_repository.get_all()

    def delete_product_record(self, product_id):
        success = self.product_repository.remove(product_id)
        if not success:
            raise ValueError(f"Delete failed: Product {product_id} not found.")
        return True


class ProductCategoryService:
    def __init__(self):
        self.category_repository = ProductCategoryRepository()

    def create_new_category(self, category_data):
        category_serializer = ProductCategorySerializer(data=category_data)

        if category_serializer.is_valid():
            return category_serializer.save()

        raise ValueError(category_serializer.errors)

    def update_existing_category(self, title, update_data):
        old_category = self.category_repository.get_by_title(title=title)
        
        if not old_category:
            raise ValueError(f"Category '{title}' not found.")
            
        category_serializer = ProductCategorySerializer(old_category, data=update_data, partial=True)
        
        if category_serializer.is_valid():
            return category_serializer.save()

        raise ValueError(category_serializer.errors)

    def get_all_categories(self):
        return self.category_repository.get_all()

    def delete_category_record(self, title):
        success = self.category_repository.remove(title)
        if not success:
            raise ValueError(f"Delete failed: Category '{title}' not found.")
        return True
    
    def get_products_by_category(self, title):
        old_category = self.category_repository.get_by_title(title=title)
        
        if not old_category:
            raise ValueError(f"Category '{title}' not found.")
            
        return self.category_repository.fetch_products(title)