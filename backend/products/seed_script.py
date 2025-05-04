# backend/scripts/seed_data.py


from backend.products.models import ProductCategory, Products

from backend.products.connection import init_mongo

init_mongo()

def seed_categories():
    ProductCategory.objects.delete()
    ProductCategory(
        category_id=1,
        category_name="Electronics",
        description="Devices and gadgets"
    ).save()
    ProductCategory(
        category_id=2,
        category_name="Clothing",
        description="Apparel and fashion"
    ).save()

def seed_products():
    Products.objects.delete()

    electronics = ProductCategory.objects.get(category_id=1)
    clothing = ProductCategory.objects.get(category_id=2)

    Products(
        product_id=1,
        name="Smartphone",
        description="A latest smartphone",
        category=electronics,
        brand="Samsung"
    ).save()

    Products(
        product_id=2,
        name="Jacket",
        description="Winter jacket",
        category=clothing,
        brand="North Face"
    ).save()

def run_seed():
    seed_categories()
    seed_products()
    print("Database seeded successfully.")

if __name__ == "__main__":
    run_seed()
