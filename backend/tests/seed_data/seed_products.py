from product.models.product_model import Product
from product.models.category import ProductCategory
from datetime import datetime

def seed_products():
    category = ProductCategory.objects(category_name="Books").first()
    
    Product(
        name="Test Book",
        description="A sample book for testing",
        brand="TestBrand",
        price_in_RS=500,
        quantity=10,
        manufacture_date=datetime(2022, 1, 1),
        expiry_date=datetime(2026, 1, 1),
        category=[category]
    ).save()
