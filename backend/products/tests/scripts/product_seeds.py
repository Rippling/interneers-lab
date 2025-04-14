# products/tests/scripts/product_seeds.py

from decimal import Decimal
from mongoengine import connect
from products.models import Product, ProductCategory

def seed_product_categories():
    """Seed product categories (should match your category seeds)"""
    connect(
        db="test_product_db",
        host="mongodb://localhost:27017/",
        alias="default"
    )
    
    # Clear existing categories
    ProductCategory.drop_collection()

    categories = [
        {"title": "Electronics", "description": "Gadgets and devices"},
        {"title": "Clothing", "description": "Apparel"},
        {"title": "Books", "description": "Reading materials"},
        {"title": "Home & Garden", "description": "Home improvement items"},
        {"title": "Sports", "description": "Sporting goods"},
        {"title": "Toys", "description": "Children's toys"},
        {"title": "Automotive", "description": "Car parts and accessories"},
    ]

    for cat in categories:
        ProductCategory(**cat).save()

    # print(f"[✔] Seeded {len(categories)} product categories")

def seed_products():
    """Seed products with category relationships"""
    connect(
        db="test_product_db",
        host="mongodb://localhost:27017/",
        alias="default"
    )

    # Clear existing products
    Product.drop_collection()

    # Get categories reference
    categories = {cat.title: cat for cat in ProductCategory.objects.all()}

    products = [
        # Electronics
        {
            "name": "Smartphone X",
            "description": "Flagship smartphone with 6.7-inch OLED display",
            "category": categories["Electronics"],
            "price": Decimal("999.99"),
            "brand": "TechMaster",
            "quantity": 100
        },
        {
            "name": "Wireless Headphones",
            "description": "Noise-cancelling over-ear headphones",
            "category": categories["Electronics"],
            "price": Decimal("249.99"),
            "brand": "SoundPro",
            "quantity": 75
        },

        # Clothing
        {
            "name": "Cotton T-Shirt",
            "description": "Plain white cotton t-shirt",
            "category": categories["Clothing"],
            "price": Decimal("19.99"),
            "brand": "FashionWear",
            "quantity": 200
        },
        {
            "name": "Men's Jeans",
            "description": "Slim-fit denim jeans",
            "category": categories["Clothing"],
            "price": Decimal("59.99"),
            "brand": "DenimCo",
            "quantity": 150
        },

        # Books
        {
            "name": "Bestseller Novel",
            "description": "Latest fiction bestseller",
            "category": categories["Books"],
            "price": Decimal("14.99"),
            "brand": "BookHouse",
            "quantity": 300
        },

        # Home & Garden
        {
            "name": "Professional Blender",
            "description": "High-powered kitchen blender",
            "category": categories["Home & Garden"],
            "price": Decimal("129.99"),
            "brand": "HomeChef",
            "quantity": 80
        },

        # Sports
        {
            "name": "Basketball",
            "description": "Official size basketball",
            "category": categories["Sports"],
            "price": Decimal("29.99"),
            "brand": "SportStar",
            "quantity": 120
        },
        {
            "name": "Running Shoes",
            "description": "Lightweight mesh running shoes",
            "category": categories["Sports"],
            "price": Decimal("89.99"),
            "brand": "RunFast",
            "quantity": 65
        },

        # Toys
        {
            "name": "LEGO City Set",
            "description": "500-piece building set",
            "category": categories["Toys"],
            "price": Decimal("49.99"),
            "brand": "LEGO",
            "quantity": 90
        },

        # Automotive
        {
            "name": "Car Wax",
            "description": "Premium car wax formula",
            "category": categories["Automotive"],
            "price": Decimal("24.99"),
            "brand": "AutoCare",
            "quantity": 200
        }
    ]

    for prod_data in products:
        Product(**prod_data).save()

    # print(f"[✔] Seeded {len(products)} products")

if __name__ == "__main__":
    seed_product_categories()
    seed_products()