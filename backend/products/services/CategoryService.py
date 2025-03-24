from ..repositories.Category import CategoryRepository

class CategoryService:
    @staticmethod
    def create_category(title, description=None):
        return CategoryRepository.create(title, description)

    @staticmethod
    def get_products_by_category_title(title):
        category = CategoryRepository.get_category_by_title(title)
        if not category:
            return None, "Category not found"

        products = CategoryRepository.get_products_by_category(category)
        return products, None
    
    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def update_category(title, new_title=None, new_description=None):
        return CategoryRepository.update(title, new_title, new_description)

    @staticmethod
    def delete_category(title):
        return CategoryRepository.delete(title)
