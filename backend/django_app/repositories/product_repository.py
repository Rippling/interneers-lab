from django_app.models.product import Product

class ProductRepository:

    @staticmethod
    def create(data):
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def get_all():
        return Product.objects.all()
    
    @staticmethod
    def get_by_id(id):
        return Product.objects(id=id).first()
    
    @staticmethod
    def update(product, data):
        product.update(**data)
        product.reload()
        return product
    
    @staticmethod
    def delete(product_id):
        product = Product.objects(id=product_id).first()
        product.delete()

    @staticmethod
    def get_by_category(category_id):
        return Product.objects(category=category_id)
    
    @staticmethod
    def get_by_name(product_name):
        return Product.objects(name=product_name).first()