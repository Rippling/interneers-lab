from products.repositories.product_repository import ProductRepository
from mongoengine.errors import DoesNotExist, ValidationError
from decimal import Decimal, InvalidOperation
from bson import ObjectId
from bson.errors import InvalidId


class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_all_products(self, sort_by=None, filters=None):
        """
        Service method to get all products with optional sorting and filtering
        """
        products = self.repository.get_all_products()
        filters = filters or {}

        # Apply filters
        category = filters.get("category")
        if category:
            try:
                ObjectId(category)
            except InvalidId:
                raise ValueError("Invalid category ID format")
            products = products.filter(category=category)

        name = filters.get("name")
        if name:
            products = products.filter(name__icontains=name)

        brand = filters.get("brand")
        if brand:
            products = products.filter(brand__icontains=brand)

        min_price = filters.get("min_price")
        if min_price is not None:
            try:
                min_price_decimal = Decimal(min_price)
            except InvalidOperation:
                raise ValueError("Invalid min_price value")
            products = products.filter(price__gte=min_price_decimal)

        max_price = filters.get("max_price")
        if max_price is not None:
            try:
                max_price_decimal = Decimal(max_price)
            except InvalidOperation:
                raise ValueError("Invalid max_price value")
            products = products.filter(price__lte=max_price_decimal)

        # Apply sorting
        if sort_by:
            allowed_sorts = {"created_at": "-created_at", "updated_at": "-updated_at"}
            if sort_by not in allowed_sorts:
                raise ValueError(
                    f"Invalid sort field. Allowed values: {', '.join(allowed_sorts.keys())}"
                )
            sort_field = allowed_sorts[sort_by]
            products = products.order_by(sort_field)

        return products

    def get_product_by_id(self, product_id):
        """
        Service method to get a product by ID
        """
        try:
            return self.repository.get_product_by_id(product_id)
        except DoesNotExist:
            raise ValueError(f"No product with id {product_id} exists.")
        except ValidationError:
            raise ValueError("Invalid ObjectId format")

    def create_product(self, product_data):
        """
        Service method to create a new product
        """
        return self.repository.create_product(product_data)

    def update_product(self, product_id, product_data):
        """
        Service method to update an existing product
        """
        try:
            product = self.repository.get_product_by_id(product_id)
            return self.repository.update_product(product, product_data)
        except DoesNotExist:
            raise ValueError(f"No product with id {product_id} exists.")
        except ValidationError:
            raise ValueError("Invalid ObjectId format")

    def delete_product(self, product_id):
        """
        Service method to delete a product
        """
        try:
            product = self.repository.get_product_by_id(product_id)
            self.repository.delete_product(product)
        except DoesNotExist:
            raise ValueError(f"No product with id {product_id} exists.")
        except ValidationError:
            raise ValueError("Invalid ObjectId format")
