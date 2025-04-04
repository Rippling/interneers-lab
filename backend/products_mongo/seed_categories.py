from products_mongo.models import ProductCategory  # Use absolute import
from products_mongo.test_connection import init_db  # Import DB connection function

# Initialize DB connection
init_db()

def seed_categories():
    categories = [
        {"title": "Electronics", "description": "Gadgets and devices"},
        {"title": "Clothing", "description": "Men and Women Apparel"},
        {"title": "Home Appliances", "description": "Household electronics"},
    ]

    for category in categories:
        if not ProductCategory.objects(title=category["title"]).first():
            ProductCategory(**category).save()
            print(f"Added category: {category['title']}")
        else:
            print(f"Category already exists: {category['title']}")

if __name__ == "__main__":
    seed_categories()
