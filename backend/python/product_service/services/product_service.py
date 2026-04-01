from bson import ObjectId

from ..repository import ProductRepository, CategoryRepository
from ..exceptions import (
    InvalidProductId,
    ProductNotFound,
    InvalidCategoryId,
    CategoryNotFound,
)


class ProductService:

    def __init__(self, product_repository=None, category_repository=None):
        self.product_repository = product_repository or ProductRepository()
        self.category_repository = category_repository or CategoryRepository()

    # ---------- CREATE ----------

    def create_product(self, data):
        return self.product_repository.create(data)

    # ---------- READ ----------

    def list_products(self, sort_by):
        return self.product_repository.get_all(sort_by)

    def get_product(self, product_id):
        self._validate_product_id(product_id)

        product = self.product_repository.get_by_id(product_id)

        if not product:
            raise ProductNotFound(product_id=product_id)

        return product

    def list_products_by_category_id(self, category_id, sort_by):
        return self.product_repository.get_all_by_category_id(category_id, sort_by)

    # ---------- UPDATE ----------

    def update_product(self, product_id, data):
        product = self.get_product(product_id)

        for key, value in data.items():

            if key == "category":
                value = self._validate_category(value)

            setattr(product, key, value)

        return self.product_repository.update(product)

    # ---------- DELETE ----------

    def delete_product(self, product_id):
        product = self.get_product(product_id)

        self.product_repository.delete(product_id)

        return product

    # ---------- HELPERS ----------

    def _validate_product_id(self, product_id):
        if not ObjectId.is_valid(product_id):
            raise InvalidProductId(product_id=product_id)

    def _validate_category(self, category_id):

        if not ObjectId.is_valid(category_id):
            raise InvalidCategoryId(category_id=category_id)

        category = self.category_repository.get_by_id(category_id)

        if not category:
            raise CategoryNotFound(category_id=category_id)

        return category