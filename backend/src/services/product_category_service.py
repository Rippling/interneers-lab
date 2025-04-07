from src.models.product_category import ProductCategory
from src.models.product import Product

#pylint: disable=no-member

class ProductCategoryService:
    """
    Service layer for managing product categories and their products.
    """

    @staticmethod
    def create_category(title: str, description: str = "") -> ProductCategory:
        """
        Creates a new product category, and saves it to the database.

        Args:
            title: Category title (must be unique).
            description: Optional description.

        Returns:
            The created ProductCategory instance.
        """
        category = ProductCategory(title=title, description=description)
        category.save()
        return category

    @staticmethod
    def get_category_by_id(category_id: str)-> ProductCategory:
        """
        Fetches a product category by ID.

        Args:
            category_id: ID of the category.

        Returns:
            ProductCategory instance.
        """
        return ProductCategory.objects.get(id=category_id)

    @staticmethod
    def get_category_by_title(category_title: int)-> ProductCategory:
        """
        Fetches a product category by title.

        Args:
            category_title: title of the category.

        Returns:
            ProductCategory instance.
        """
        return ProductCategory.objects.get(title= category_title)

    @staticmethod
    def update_category(category_title: str, title: str= None, description: str= None) \
    -> ProductCategory:
        """
        Updates a product category's title or description.

        Args:
            category_title: title of the category.
            title: New title (if updating).
            description: New description (if updating).

        Returns:
            Updated ProductCategory instance.
        """
        category = ProductCategory.objects.get(title= category_title)
        if title is not None:
            category.title= title
        if description is not None:
            category.description= description
        category.save()
        return category

    @staticmethod
    def delete_category(category_id: str):
        """
        Deletes a product category.

        Args:
            category_id: ID of the category.

        Returns:
            None.
        """
        category = ProductCategory.objects.get(id=category_id)
        category.delete()

    @staticmethod
    def list_products_in_category(category_id: str):
        """
        Lists all products belonging to a category.

        Args:
            category_id: ID of the category.

        Returns:
            List of Product instances in the category.
        """
        return Product.objects(category=category_id)

    @staticmethod
    def add_product_to_category(product_id: str, category_id: str):
        """
        Adds a product to a category.

        Args:
            product_id: ID of the product.
            category_id: ID of the category.

        Returns:
            Updated Product instance.
        """
        product = Product.objects.get(id=product_id)
        category = ProductCategory.objects.get(id=category_id)
        product.category = category
        product.save()
        return product

    @staticmethod
    def remove_product_from_category(product_id: str):
        """
        Removes a product from its category.

        Args:
            product_id: ID of the product.

        Returns:
            Updated Product instance.
        """
        product = Product.objects.get(id=product_id)
        product.category = None
        product.save()
        return product
