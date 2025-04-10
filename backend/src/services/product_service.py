from src.models.product import Product  # Assuming the Product model is in models/product.py

#pylint: disable=no-member

class ProductService:
    """
    Service layer for managing products in the database.
    """

    @staticmethod
    def create_product(data: dict) -> Product:
        """
        Creates a new product and saves it to the database.

        Args:
            data: Dictionary containing product details. Required keys: "name", "price", "quantity".
                  Optional keys: "brand", "description".
        
        Returns:
            Created Product instance.
        """
        product = Product(
            name=data["name"],
            price=data["price"],
            quantity=data["quantity"],
            brand=data.get("brand", ""),  # Default to empty string
            description=data.get("description", "")
        )
        product.save()
        return product

    @staticmethod
    def get_product_by_id(product_id: str) -> Product:
        """
        Fetches a product by its ID.

        Args:
            product_id: The ID of the product to fetch.

        Returns:
            Product instance if found.
        
        Raises:
            DoesNotExist: If the product does not exist.
        """
        return Product.objects.get(id=product_id)

    @staticmethod
    def update_product(product_id: str, data: dict) -> Product:
        """
        Updates specified fields of a product.

        Args:
            product_id: The ID of the product to update.
            data: Dictionary containing fields to update.

        Returns:
            Updated Product instance.
        
        Raises:
            DoesNotExist: If the product does not exist.
            KeyError: If an invalid field is provided.
        """
        product = Product.objects.get(id=product_id)
        product.modify_fields(data)
        return product

    @staticmethod
    def delete_product(product_id: str) -> None:
        """
        Deletes a product from the database.

        Args:
            product_id: The ID of the product to delete.
        
        Raises:
            DoesNotExist: If the product does not exist.
        """
        product = Product.objects.get(id=product_id)
        product.delete()

    @staticmethod
    def modify_stock(product_id: str, amount: int) -> int:
        """
        Modifies the stock of a product.

        Args:
            product_id: The ID of the product.
            amount: The amount to adjust the stock by (positive or negative).

        Returns:
            Updated stock quantity.
        
        Raises:
            DoesNotExist: If the product does not exist.
            ValueError: If stock would go negative.
        """
        product = Product.objects.get(id=product_id)
        return product.modify_stock(amount)

    @staticmethod
    def set_stock(product_id: str, amount: int) -> int:
        """
        Sets the stock of a product.

        Args:
            product_id: The ID of the product.
            amount: The new stock amount.

        Returns:
            Updated stock quantity.
        
        Raises:
            DoesNotExist: If the product does not exist.
            ValueError: If stock amount is negative.
        """
        product = Product.objects.get(id=product_id)
        return product.set_stock(amount)

    @staticmethod
    def set_price(product_id: str, amount: int) -> int:
        """
        Updates the price of a product.

        Args:
            product_id: The ID of the product.
            amount: The new price amount.

        Returns:
            Updated price.
        
        Raises:
            DoesNotExist: If the product does not exist.
            ValueError: If price amount is negative.
        """
        product = Product.objects.get(id=product_id)
        return product.set_price(amount)
