from ..repositories.product_category_repository import ProductCategoryRepository

class ProductCategoryService:
    def __init__(self):
        self.repository = ProductCategoryRepository()

    def get_all_categories(self):
        """Get all categories"""
        return self.repository.get_all()

    def get_category_by_id(self, category_id):
        """Get single category by ID"""
        return self.repository.get_by_id(category_id)

    def create_category(self, category_data):
        """Create new category with validation"""
        if self.repository.get_by_title(category_data.get('title')):
            raise ValueError("Category title already exists")
        
        return self.repository.create(category_data)

    def update_category(self, category_id, category_data):
        """Update existing category with validation"""
        if 'title' in category_data:
            existing = self.repository.get_by_title(category_data['title'])
            if existing and str(existing.id) != category_id:
                raise ValueError("Category title must be unique")
        
        return self.repository.update(category_id, category_data)

    def delete_category(self, category_id):
        """Delete category"""
        return self.repository.delete(category_id)
