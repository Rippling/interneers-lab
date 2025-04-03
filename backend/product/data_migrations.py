from models.product_model import Product
from mongoengine import connect

connect("product_db", host="mongodb://localhost:27017/product_db")

# Default brand name
DEFAULT_BRAND = "Unknown"

products_without_brand = Product.objects(brand=None) or Product.objects(brand="")

for product in products_without_brand:
    product.brand = DEFAULT_BRAND
    product.save()

print(f"Updated {len(products_without_brand)} products with default brand '{DEFAULT_BRAND}'.")
