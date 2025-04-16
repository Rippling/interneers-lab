import mongoengine
from products.models.ProductModel import ProductCategory, Product
from decimal import Decimal

def seed_database():
    
    # Clear existing data
    ProductCategory.objects.delete()
    Product.objects.delete()
    
    # Create categories
    electronics = ProductCategory(
        title="Electronics",
        description="Electronic devices and accessories"
    ).save()
    
    clothing = ProductCategory(
        title="Clothing",
        description="Apparel and fashion items"
    ).save()
    
    furniture = ProductCategory(
        title="Furniture",
        description="Home and office furniture"
    ).save()
    
    # Create products
    smartphone = Product(
        name="Smartphone X",
        description="Latest smartphone with advanced features",
        brand="TechBrand",
        category=[electronics],
        price=Decimal('799.99'),
        quantity=50
    ).save()
    
    laptop = Product(
        name="Laptop Pro",
        description="Professional laptop for developers",
        brand="CodeMaster",
        category=[electronics],
        price=Decimal('1299.99'),
        quantity=30
    ).save()
    
    tshirt = Product(
        name="Cotton T-Shirt",
        description="Comfortable cotton t-shirt",
        brand="FashionCo",
        category=[clothing],
        price=Decimal('19.99'),
        quantity=200
    ).save()
    
    desk = Product(
        name="Office Desk",
        description="Ergonomic office desk",
        brand="OfficePro",
        category=[furniture],
        price=Decimal('249.99'),
        quantity=15
    ).save()
    
    smartwatch = Product(
        name="Smart Watch",
        description="Fitness and notification tracking",
        brand="TechBrand",
        category=[electronics, clothing],  # Cross-category product
        price=Decimal('199.99'),
        quantity=45
    ).save()
    
    return {
        "categories": {
            "electronics": electronics,
            "clothing": clothing,
            "furniture": furniture
        },
        "products": {
            "smartphone": smartphone,
            "laptop": laptop,
            "tshirt": tshirt,
            "desk": desk,
            "smartwatch": smartwatch
        }
    }