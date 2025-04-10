from products_mongo.models import Product, ProductCategory
from products_mongo.test_connection import init_db

init_db

def seed_data():
    """Populate test database with initial data for integration testing."""
    
    Product.objects.delete()
    ProductCategory.objects.delete()

    category1 = ProductCategory(title="Electronics", description="Gadgets and devices")
    category1.save()

    category2 = ProductCategory(title="Clothing", description="Men and Women Fashion")
    category2.save()

    # Create sample products
    product1 = Product(
        name="Smartphone",
        description="A high-end smartphone",
        price=699.99,
        brand="TechCorp",
        quantity_in_warehouse=50,
        category=category1
    )
    product1.save()

    product2 = Product(
        name="T-Shirt",
        description="Cotton t-shirt",
        price=19.99,
        brand="FashionWear",
        quantity_in_warehouse=200,
        category=category2
    )
    product2.save()

    print("Seed data inserted successfully.")

if __name__ == "__main__":
    seed_data()
