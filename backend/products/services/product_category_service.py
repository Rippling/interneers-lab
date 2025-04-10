class ProductCategoryService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_categories(self):
        """Get all categories"""
        return self.repository.get_all()

    def get_category_by_id(self, category_id):
        """Get single category by ID"""
        return self.repository.get_by_id(category_id)

    def get_category_by_title(self, title):
        """Get single category by title"""
        return self.repository.get_by_title(title)

    def create_category(self, category_data):
        """Create new category with validation"""
        # category data is a instance of ProductCategoryDetail dataclass
        if self.repository.get_by_title(category_data.title):
            raise ValueError("Category title already exists")

        return self.repository.create(category_data)

    def update_category(self, category_id: str, category_data):
        """Update existing category with validation"""

        # Check if title is being changed and ensure uniqueness
        if category_data.title:
            existing = self.repository.get_by_title(category_data.title)
            if existing and str(existing.id) != category_id:
                raise ValueError("Category title must be unique")

        return self.repository.update(category_id, category_data)
        

    def delete_category(self, category_id):
        """Delete category"""
        return self.repository.delete(category_id)
