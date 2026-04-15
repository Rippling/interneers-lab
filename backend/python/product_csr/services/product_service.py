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

    def get_products_by_category(self, category_id, owner_id):
        category = self.category_repo.get_by_id(category_id, owner_id=owner_id)
        if not category:
            raise ValueError("Category not found")

        products = self.repo.get_by_category(category, owner_id=owner_id)
        return [product.to_dict() for product in products]

    def add_product_to_category(self, product_id, category_id, owner_id):
        product = self.repo.get_by_id(product_id)
        category = self.category_repo.get_by_id(category_id, owner_id=owner_id)

        if not product:
            raise ValueError("Product not found")
        if not category:
            raise ValueError("Category not found")
        if str(product.owner_id) != str(owner_id):
            raise ValueError("You are not allowed to move this product")

        product.category = category
        product.save()

        return {"message": "Product added to category"}

    def remove_product_from_category(self, product_id, owner_id):
        product = self.repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")
        if str(product.owner_id) != str(owner_id):
            raise ValueError("You are not allowed to modify this product")

        product.category = None
        product.save()

        return {"message": "Product removed from category"}

    def create_product(self, data, owner_id):
        required_fields = ["name", "price", "brand", "quantity"]

        for field in required_fields:
            if field not in data or data.get(field) in (None, ""):
                raise ValueError(f"{field} is required")

        if data["price"] <= 0:
            raise ValueError("Price must be positive")

        if data["quantity"] < 0:
            raise ValueError("Quantity cannot be negative")

        category_id = data.get("category") or data.get("category_id") or data.get("categoryId")
        if category_id:
            category = self.category_repo.get_by_id(category_id, owner_id=owner_id)
            if not category:
                raise ValueError("Category not found")
            data["category"] = category
        else:
            data["category"] = None

        data.pop("category_id", None)
        data.pop("categoryId", None)
        data["image_url"] = data.pop("imageUrl", data.get("image_url", ""))
        data["owner_id"] = str(owner_id)

        product = self.repo.create(data)
        return product.to_dict()

    def get_all_products(self, owner_id, filters=None):
        filters = filters or {}
        normalized_filters = {
            key: value for key, value in filters.items()
            if value not in (None, "")
        }

        if not normalized_filters:
            products = self.repo.get_all(owner_id=owner_id)
        else:
            products = self.repo.filter_products(normalized_filters, owner_id=owner_id)

        return [product.to_dict() for product in products]

    def update_product(self, product_id, data, owner_id):
        product = self.repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")
        if str(product.owner_id) != str(owner_id):
            raise ValueError("You are not allowed to update this product")

        if "brand" in data and not data.get("brand"):
            raise ValueError("Brand cannot be empty")

        if "price" in data and data["price"] <= 0:
            raise ValueError("Price must be positive")

        if "quantity" in data and data["quantity"] < 0:
            raise ValueError("Quantity cannot be negative")

        if "category" in data or "category_id" in data or "categoryId" in data:
            category_id = data.get("category") or data.get("category_id") or data.get("categoryId")
            if category_id:
                category = self.category_repo.get_by_id(category_id, owner_id=owner_id)
                if not category:
                    raise ValueError("Category not found")
                data["category"] = category
            else:
                data["category"] = None

        data.pop("category_id", None)
        data.pop("categoryId", None)
        if "imageUrl" in data:
            data["image_url"] = data.pop("imageUrl")

        updated_product = self.repo.update(product, data)
        return updated_product.to_dict()

    def delete_product(self, product_id, owner_id):
        product = self.repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")
        if str(product.owner_id) != str(owner_id):
            raise ValueError("You are not allowed to delete this product")

        self.repo.delete(product)
        return {"message": "Product deleted successfully"}
