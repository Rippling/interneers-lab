from products_mongo.models import Product, ProductCategory # Use absolute import
from products_mongo.test_connection import init_db  # Import DB connection function

# Initialize DB connection
init_db()

def migrate_products():
    # Check if "Uncategorized" category exists
    default_category = ProductCategory.objects(title="Uncategorized").first()
    
    # If not found, create it
    if not default_category:
        default_category = ProductCategory(title="Uncategorized", description="Products without a specific category")
        default_category.save()
        print("Created 'Uncategorized' category.")

    # Find all products without a category
    products_without_category = Product.objects(category=None)

    for product in products_without_category:
        product.category = default_category  # Assign the default category
        product.save()
        print(f"Assigned 'Uncategorized' category to {product.name}")

if __name__ == "__main__":
    migrate_products()
