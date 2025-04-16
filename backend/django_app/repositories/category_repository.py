from django_app.models.category import Category

class CategoryRepository:

    @staticmethod
    def create(category_data):
        category = Category(**category_data)
        category.save()
        return category
    
    @staticmethod
    def get_all():
        return Category.objects.all()
    
    @staticmethod
    def get_by_id(id):
        return Category.objects(id=id).first()
    
    @staticmethod
    def update(category, data):
        category.update(**data)
        category.reload()
        return category
    
    @staticmethod
    def delete(category_id):
        category = Category.objects(id=category_id).first()
        category.delete()

    @staticmethod
    def get_by_title(title):
        return Category.objects(title=title).first()