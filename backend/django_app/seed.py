from bson import DBRef
from django_app.models import Product, ProductCategory
from mongoengine import connect

connect(db="your_database_name", host="localhost", port=27017)

def seed_data():
    # Create initial categories
    categories = [
        {"title": "Electronics", "description": "Gadgets and devices"},
        {"title": "Cosmetics", "description": "Beauty and skin-care"},
    ]

    for category_data in categories:
        category = ProductCategory.objects(title=category_data["title"]).first()
        if not category:
            category = ProductCategory(**category_data)
            category.save()

    # Create initial products
    products = [
        {
            "name": "iPhone",
            "description": "Great camera and performance",
            "category": "Electronics",
            "price": 70000,
            "brand": "Apple",
            "quantity": 5
        },
        {
            "name": "Face Cream",
            "description": "Soft and smooth skin",
            "category": "Cosmetics",
            "price": 500,
            "brand": "Fair & Lovely",
            "quantity": 20
        }
    ]

    for product_data in products:
        category = ProductCategory.objects(title=product_data["category"]).first()
        if category:
            product_data["category"] = {
                "_ref": DBRef("product_category", category.id),
                "title": category.title,
                "description": category.description,
            }
        if not Product.objects(name=product_data["name"]).first():
            product = Product(**product_data)
            product.save()
            
def create_sample_category(title="Electronics", description="Electronic items"):
    category = ProductCategory.objects(title=title).first()
    if not category:
        category = ProductCategory(title=title, description=description)
        category.save()
    return category

def create_sample_product(category, name="iPhone", price=79999):
    if Product.objects(name=name).first():
        return Product.objects(name=name).first()

    product = Product(
        name=name,
        description="Latest iPhone",
        category={
            "_ref": DBRef("product_category", category.id),
            "title": category.title,
            "description": category.description,
        },
        price=price,
        brand="Apple",
        quantity=10
    )
    product.save()
    return product


if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully!")
