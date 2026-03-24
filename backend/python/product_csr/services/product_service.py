from product_csr.ports.product_repository_port import ProductRepositoryPort
from product_csr.ports.category_repository_port import CategoryRepositoryPort


class ProductService:
    def __init__(
        self,
        repo: ProductRepositoryPort,
        category_repo: CategoryRepositoryPort,
    ):
        self.repo = repo
        self.category_repo = category_repo

    def get_products_by_category(self, category_id):
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        products = self.repo.get_by_category(category)
        return [product.to_dict() for product in products]

    def add_product_to_category(self, product_id, category_id):
        product = self.repo.get_by_id(product_id)
        category = self.category_repo.get_by_id(category_id)

        if not product:
            raise ValueError("Product not found")
        if not category:
            raise ValueError("Category not found")

        product.category = category
        product.save()

        return {"message": "Product added to category"}

    def remove_product_from_category(self, product_id):
        product = self.repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")

        product.category = None
        product.save()

        return {"message": "Product removed from category"}

    def create_product(self, data):
        required_fields = ["name", "price", "brand", "quantity"]

        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"{field} is required")

        if data["price"] <= 0:
            raise ValueError("Price must be positive")

        product = self.repo.create(data)
        return product.to_dict()

    def get_all_products(self, filters=None):
        filters = filters or {}
        normalized_filters = {
            key: value for key, value in filters.items()
            if value not in (None, "")
        }

        if not normalized_filters:
            products = self.repo.get_all()
        else:
            products = self.repo.filter_products(normalized_filters)

        return [product.to_dict() for product in products]

    def update_product(self, product_id, data):
        product = self.repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")

        if "brand" in data and not data.get("brand"):
            raise ValueError("Brand cannot be empty")

        if "price" in data and data["price"] <= 0:
            raise ValueError("Price must be positive")

        updated_product = self.repo.update(product, data)
        return updated_product.to_dict()

    def delete_product(self, product_id):
        product = self.repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")

        self.repo.delete(product)
        return {"message": "Product deleted successfully"}
