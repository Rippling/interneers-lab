from productAPI.repositories import ProductCategoryRepository
from productAPI.repositories import ProductRepository
from django.core.paginator import Paginator
from productAPI.constants import DEFAULT_CATEGORY_PAGE_SIZE as pgsz


class ProductCategoryService:
    
    @staticmethod
    def get_categories(page_number = None):
        categories = ProductCategoryRepository.get_all()
        
        if page_number:
            paginator = Paginator(categories, pgsz)
            page=paginator.get_page(page_number)
            return page
        return categories
    
    @staticmethod
    def create_category(validated_data):
        return ProductCategoryRepository.create(validated_data)
        
    @staticmethod
    def update_category(category_id, validated_data):
        category=ProductCategoryRepository.get_by_id(category_id)
        
        if not category:
            return None
        
        return ProductCategoryRepository.update(category, validated_data)
    
    @staticmethod
    def delete_category(category_id):
        category = ProductCategoryRepository.get_by_id(category_id)
        
        if not category:
            return None
        
        ProductCategoryRepository.delete(category)
        
        return True
    
    @staticmethod
    def get_products_by_category(category_id):
        
        products = ProductRepository.get_products_by_category(category_id)
        
        return products
    
    