from products.models import Product
from mongoengine.errors import DoesNotExist, ValidationError

class ProductRepository:
    def get_all_products(self):
        """
        Retrieve all products from the database
        """
        return Product.objects.all()
    
    def get_product_by_id(self, product_id):
        """
        Retrieve a product by its ID
        """
        try:
            return Product.objects.get(id=product_id)
        except (DoesNotExist, ValidationError) as e:
            raise e
    
    def create_product(self, product_data):
        """
        Create a new product in the database
        """
        product = Product(**product_data)
        product.save()
        return product
    
    def update_product(self, product, product_data):
        """
        Update an existing product in the database
        """
        for key, value in product_data.items():
            setattr(product, key, value)
        product.save()
        return product
    
    def delete_product(self, product):
        """
        Delete a product from the database
        """
        product.delete()