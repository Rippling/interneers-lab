from .models import ProductCategory

class ProductCategoryRepository:
    @staticmethod
    def create(data):
        product_category = ProductCategory(**data)
        product_category.save()
        return product_category

    @staticmethod
    def get_all():
        return ProductCategory.objects()

    @staticmethod
    def get_by_id(product_category_id):
        return ProductCategory.objects(id=product_category_id).first()

    @staticmethod
    def update(product_category_id, data):
        product_category = ProductCategory.objects(id=product_category_id).first()
        if product_category:
            for key, value in data.items():
                setattr(product_category, key, value)
            product_category.save()
        return product_category

    @staticmethod
    def delete(product_category_id):
        product_category = ProductCategory.objects(id=product_category_id).first()
        if product_category:
            product_category.delete()
        return product_category

