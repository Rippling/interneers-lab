from django_app.repositories.category_repository import CategoryRepository
from django_app.serializers.category_serializer import CategorySerializer
from django.utils import timezone

class CategoryService:

    @staticmethod
    def create_category(category_data):
        category = CategoryRepository.create(category_data)
        return CategorySerializer(category).data
            
    @staticmethod
    def get_all_categories(ordering=None, filters=None):
        categories = CategoryRepository.get_all()
        if filters:
            if 'created_after' in filters:
                categories = categories.filter(created_at__gte=filters['created_after'])
            if 'created_before' in filters:
                categories = categories.filter(created_at__lte=filters['created_before'])
            if 'updated_after' in filters:
                categories = categories.filter(updated_at__gte=filters['updated_after'])
            if 'updated_before' in filters:
                categories = categories.filter(updated_at__lte=filters['updated_before'])
        if ordering:
            categories = categories.order_by(ordering)
        return CategorySerializer(categories, many=True).data
    
    @staticmethod 
    def get_category_by_id(pk):
        category = CategoryRepository.get_by_id(pk)
        if not category:
            return None
        return CategorySerializer(category).data
    
    @staticmethod
    def update_category(category_data, pk):
        category = CategoryRepository.get_by_id(pk)
        if not category:
            return None
        category_data["updated_at"] = timezone.now()
        updated_category = CategoryRepository.update(category, category_data)
        return CategorySerializer(updated_category).data
    
    @staticmethod
    def delete_category(category_id):
        CategoryRepository.delete(category_id)

    @staticmethod
    def get_category_by_title(category_title):
        category = CategoryRepository.get_by_title(category_title)
        if not category:
            return None
        return CategorySerializer(category).data
