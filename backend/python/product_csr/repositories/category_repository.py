from product_csr.models import ProductCategory
from product_csr.ports.category_repository_port import CategoryRepositoryPort


class MongoCategoryRepository(CategoryRepositoryPort):
    def get_all(self):
        return ProductCategory.objects()

    def get_by_id(self, category_id):
        return ProductCategory.objects(id=category_id).first()

    def create(self, data):
        category = ProductCategory(**data)
        category.save()
        return category

    def update(self, category, data):
        category.title = data.get("title", category.title)
        category.description = data.get("description", category.description)
        category.save()
        return category

    def delete(self, category):
        category.delete()
        return True

    def get_by_title(self, title):
        return ProductCategory.objects(title=title).first()
