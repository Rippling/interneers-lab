from .models import Product
from datetime import datetime
import pytz

class ProductRepository:
    @staticmethod
    def create_product(data):
        data["created_at"] = datetime.now(pytz.utc)
        data["updated_at"] = datetime.now(pytz.utc)
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects(id=product_id).first()

    @staticmethod
    def get_all_products():
        return list(Product.objects())

    @staticmethod
    def update_product(product_id, updated_fields):
        updated_fields["updated_at"] = datetime.now(pytz.utc)  # Update timestamp

        update_query = {"set__" + field_name: new_value for field_name, new_value in updated_fields.items()}
        result = Product.objects(id=product_id).update_one(**update_query)
        return Product.objects(id=product_id).first() if result else None

    @staticmethod
    def delete_product(product_id):
        result = Product.objects(id=product_id).delete()
        return result > 0  
