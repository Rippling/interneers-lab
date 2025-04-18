import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
import django
django.setup()

from mongoengine import connect, disconnect
from product.models.product import Product
from product.models.product_category import ProductCategory

def seed():
    # Disconnect any existing connections
    disconnect()
    # Connect to the test database 'test_db'
    connect(db='test_db', host='localhost', port=27017)

    # Clear out existing data
    Product.drop_collection()
    ProductCategory.drop_collection()

    # Create sample categories
    electronics = ProductCategory(
        title="Electronics",
        description="Electronic gadgets and devices"
    )
    electronics.save()

    books = ProductCategory(
        title="Books",
        description="A variety of books and literature"
    )
    books.save()

    # Create sample products with category references
    product1 = Product(
        name="Laptop",
        description="A powerful laptop with high performance",
        price=233.1,
        brand="BrandA",
        quantity=10,
        category=electronics
    )
    product1.save()

    product2 = Product(
        name="Smartphone",
        description="A smartphone with a great camera and long battery life",
        price=499.99,
        brand="BrandB",
        quantity=25,
        category=electronics 
    )
    product2.save()
    
    product3 = Product(
        name="Python Programming",
        description="An introductory book on Python programming",
        price=29.99,
        brand="BrandC",
        quantity=100,
        category=books  
    )
    product3.save()

    print("Seeding completed! 'test_db' now has sample categories and products.")

if __name__ == '__main__':
    seed()
