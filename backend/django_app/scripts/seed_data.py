import os
import sys
import django
from django.utils import timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

from django_app.models.product import Product
from django_app.models.category import Category


def seed_categories():
    Category.objects.delete()

    electronics = Category(title="Electronics", description="Devices, gadgets, and accessories")
    clothing = Category(title="Clothing", description="Men's and women's fashion wear")
    home_appliances = Category(title="Home Appliances", description="Kitchen and home use appliances")
    books = Category(title="Books", description="All genres of books")

    electronics.save()
    clothing.save()
    home_appliances.save()
    books.save()

    categories = {
        "Electronics": electronics,
        "Clothing": clothing,
        "Home Appliances": home_appliances,
        "Books": books,
    }
    return categories


def seed_products(categories):
    Product.objects.delete()

    Product(
        name="iPhone 14", brand="Apple", price=999.99, quantity=10,
        category=categories["Electronics"], created_at=timezone.now(), updated_at=timezone.now()
    ).save()

    Product(
        name="T-shirt", brand="H&M", price=19.99, quantity=50,
        category=categories["Clothing"], created_at=timezone.now(), updated_at=timezone.now()
    ).save()

    Product(
        name="Microwave Oven", brand="LG", price=120.50, quantity=20,
        category=categories["Home Appliances"], created_at=timezone.now(), updated_at=timezone.now()
    ).save()

    Product(
        name="Harry Potter", brand="Bloomsbury", price=29.99, quantity=100,
        category=categories["Books"], created_at=timezone.now(), updated_at=timezone.now()
    ).save()


if __name__ == "__main__":
    categories = seed_categories()
    seed_products(categories)
