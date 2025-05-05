from .repository import ProductRepository, CategoryRepository
from .models import Product, Category
from mongoengine.errors import ValidationError as MongoValidationError

class CategoryService:
    @staticmethod
    def get_category_by_slug(slug):
        return CategoryRepository.get_by_slug(slug)

    @staticmethod
    def get_category_by_id(id):
        return CategoryRepository.get_by_id(id)

    @staticmethod
    def list_categories():
        return CategoryRepository.list_all()

    @staticmethod
    def create_category(data):
        return CategoryRepository.create(data)

    @staticmethod
    def delete_category(category):
        CategoryRepository.delete(category)

class ProductService:
    @staticmethod
    def get_product_by_slug(slug):
        return ProductRepository.get_by_slug(slug)

    @staticmethod
    def get_product_by_id(id):
        return ProductRepository.get_by_id(id)

    @staticmethod
    def list_products(filters=None):
        return ProductRepository.list_all(filters)

    @staticmethod
    def create_product(data):
        try:
            return ProductRepository.create(data)
        except MongoValidationError as e:
            raise ValueError(str(e))

    @staticmethod
    def update_product(product, data):
        try:
            return ProductRepository.update(product, data)
        except MongoValidationError as e:
            raise ValueError(str(e))

    @staticmethod
    def delete_product(product):
        ProductRepository.delete(product)

    @staticmethod
    def filter_products_by_category(category_slug):
        category = CategoryRepository.get_by_slug(category_slug)
        if not category:
            return []
        return Product.objects(category=category)

    @staticmethod
    def filter_products_by_status(status):
        return Product.objects(status=status)

    @staticmethod
    def filter_products_by_stock(stock_status):
        if stock_status == 'in_stock':
            return Product.objects(quantity__gt=0)
        elif stock_status == 'out_of_stock':
            return Product.objects(quantity=0)
        elif stock_status == 'low_stock':
            return [p for p in Product.objects(quantity__gt=0) if p.quantity <= p.low_stock_threshold]
        return Product.objects()
