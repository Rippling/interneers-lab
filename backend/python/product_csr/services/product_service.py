from product_csr.repositories.product_repository import ProductRepository
from product_csr.repositories.category_repository import CategoryRepository
from product_csr.models import ProductCategory


class ProductService:

    def __init__(self):
        self.repo = ProductRepository()
        self.category_repo = CategoryRepository() 


    # Get products by category
    def get_products_by_category(self, category_id):
        category = self.category_repo.get_by_id(category_id)
        if not category:
            raise ValueError("Category not found")

        products = self.repo.get_by_category(category)
        return [p.to_dict() for p in products]


    # Add product to category
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


    # Remove product from category
    def remove_product_from_category(self, product_id):
        product = self.repo.get_by_id(product_id)

        if not product:
            raise ValueError("Product not found")

        product.category = None
        product.save()

        return {"message": "Product removed from category"}

    # create product
    def create_product(self, data):

        required_fields = ["name", "price", "brand", "quantity"]

        for field in required_fields:
            if not data.get(field):   # 🔥 better validation
                raise ValueError(f"{field} is required")

        if data["price"] <= 0:
            raise ValueError("Price must be positive")

        return self.repo.create(data).to_dict()


    # get all product based on filetrs 
    def get_all_products(self, filters=None):
      filters = filters or {}

      if not filters:
        products = self.repo.get_all()
      else:
        products = self.repo.filter_products(filters)

      return [p.to_dict() for p in products]


    # update product
    def update_product(self, product_id, data):

      product = self.repo.get_by_id(product_id)

      if not product:
        raise ValueError("Product not found")

    #  Validation
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