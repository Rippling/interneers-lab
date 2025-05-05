import os
import django
import mongoengine
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

# Import models after Django setup
from products.models import Category, Product

def add_test_data():
    # Clear existing data
    print("Clearing existing data...")
    Category.objects.delete()
    Product.objects.delete()
    
    # Create categories
    print("Creating categories...")
    electronics = Category(
        name="Electronics",
        description="Electronic devices and gadgets"
    ).save()
    
    clothing = Category(
        name="Clothing", 
        description="Apparel, shoes, and accessories"
    ).save()
    
    home_kitchen = Category(
        name="Home & Kitchen",
        description="Furniture, appliances, and home decor"
    ).save()
    
    # Create products for Electronics
    print("Creating electronics products...")
    Product(
        sku="ELE-12345",
        name="Smartphone XYZ",
        description="Latest smartphone with advanced features",
        category=electronics,
        brand="TechCorp",
        tags=["smartphone", "mobile", "tech"],
        price=Decimal('699.99'),
        quantity=50,
        low_stock_threshold=10,
        status="active",
        featured=True
    ).save()
    
    Product(
        sku="ELE-23456",
        name="Laptop Pro",
        description="High-performance laptop for professionals",
        category=electronics,
        brand="ComputeMaster",
        tags=["laptop", "computer", "tech"],
        price=Decimal('1299.99'),
        quantity=20,
        low_stock_threshold=5,
        status="active",
        featured=True
    ).save()
    
    Product(
        sku="ELE-34567",
        name="Wireless Headphones",
        description="Noise-cancelling bluetooth headphones",
        category=electronics,
        brand="AudioTech",
        tags=["headphones", "audio", "wireless"],
        price=Decimal('149.99'),
        quantity=30,
        status="active"
    ).save()
    
    # Create products for Clothing
    print("Creating clothing products...")
    Product(
        sku="CLC-12345",
        name="Men's T-Shirt",
        description="Comfortable cotton t-shirt",
        category=clothing,
        brand="FashionCo",
        tags=["men", "t-shirt", "casual"],
        price=Decimal('24.99'),
        quantity=100,
        status="active"
    ).save()
    
    Product(
        sku="CLC-23456",
        name="Women's Dress",
        description="Elegant summer dress",
        category=clothing,
        brand="StyleWear",
        tags=["women", "dress", "summer"],
        price=Decimal('59.99'),
        quantity=4,
        low_stock_threshold=10,
        status="active"
    ).save()
    
    # Create products for Home & Kitchen
    print("Creating home & kitchen products...")
    Product(
        sku="HMK-12345",
        name="Coffee Maker",
        description="Programmable coffee maker with timer",
        category=home_kitchen,
        brand="HomeBrew",
        tags=["kitchen", "appliance", "coffee"],
        price=Decimal('79.99'),
        quantity=25,
        status="active"
    ).save()
    
    Product(
        sku="HMK-23456",
        name="Sofa Set",
        description="3-piece living room sofa set",
        category=home_kitchen,
        brand="ComfortLiving",
        tags=["furniture", "living room"],
        price=Decimal('899.99'),
        quantity=0,
        status="out_of_stock"
    ).save()
    
    print("Test data added successfully!")

if __name__ == "__main__":
    add_test_data() 