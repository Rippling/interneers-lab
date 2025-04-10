from typing import Optional
from products.models import Product, ProductCategory
from mongoengine.errors import DoesNotExist, ValidationError
from dataclasses import dataclass, asdict


@dataclass
class ProductDetail:
    name: str
    description: str
    price: float
    category: str
    brand: str
    quantity: int = 0
    id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


    @classmethod
    def from_product_model(cls, product_model):
        """Convert Product model to ProductDetail"""
        return cls(
            id=str(product_model.id) if product_model.id else None,
            name=product_model.name,
            description=product_model.description,
            price=float(product_model.price),
            category=str(product_model.category.title) if product_model.category else None,
            brand=product_model.brand,
            quantity=product_model.quantity,
            created_at=product_model.created_at.isoformat(),
            updated_at=product_model.updated_at.isoformat()
        )


class ProductRepository:
    def get_all_products(self):
        """
        Retrieve all products from the database
        """
        try:
            products = Product.objects.all()

            return [ProductDetail.from_product_model(prod) for prod in products]
        except Exception as e:
            raise ValueError(f"An error occurred while fetching products: {str(e)}")

    def get_product_by_id(self, product_id):
        """
        Retrieve a product by its ID
        """
        try:
            product = Product.objects.get(id=product_id)
            return ProductDetail.from_product_model(product)
        except DoesNotExist:
            raise ValueError(f"Product with id {product_id} not found")
        except ValidationError as e:
            raise ValueError(f"Invalid product ID: {str(e)}")

    def create_product(self, product_data: ProductDetail):
        """
        Create a new product in the database
        """
        try:
            
            
            category = ProductCategory.objects(title=product_data.category).first()

            create_data = asdict(product_data)
            create_data.pop("id", None)  
            create_data["category"] = category  

            product = Product(**create_data).save()
            return ProductDetail.from_product_model(product)

        except Exception as e:
            raise ValueError(f"An error occurred while creating the product: {str(e)}")

    def update_product(self, product_id, product_data: ProductDetail):
        """
        Update an existing product in the database
        """
        try:
            product = Product.objects.get(id=product_id)
            category = ProductCategory.objects(title=product_data.category).first()

            update_data = asdict(product_data)

            update_data.pop("id", None)  
            update_data["category"] = category  

            product.update(**update_data)
            product.reload()

            return ProductDetail.from_product_model(product)

        except DoesNotExist:
            raise ValueError(f"Product with id {product_id} not found")
        except ValidationError as e:
            raise ValueError(f"Invalid product ID: {str(e)}")

    def delete_product(self, product_id):
        """
        Delete a product from the database
        """
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
        except DoesNotExist:
            raise ValueError(f"Product with id {product_id} not found")
        except ValidationError as e:
            
            raise ValueError(f"Invalid product ID: {str(e)}")
