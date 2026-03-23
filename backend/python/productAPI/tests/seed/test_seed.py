# productAPI/tests/seed/test_seed.py

from productAPI.models import Product, ProductCategory


def seed_categories():
    
    food = ProductCategory(
        title="Food",
        description="Edible products and groceries"
    )
    food.save()

    electronics = ProductCategory(
        title="Electronics",
        description="Gadgets and devices"
    )
    electronics.save()

    uncategorized = ProductCategory(
        title="Uncategorized",
        description="Products without a category"
    )
    uncategorized.save()

    return {
        "food": food,
        "electronics": electronics,
        "uncategorized": uncategorized
    }


def seed_products(categories):
    
    milk = Product(
        name="Milk",
        brand="Amul",
        price=50,
        quantity=100,
        description="Fresh dairy milk",
        category=categories["food"]
    )
    milk.save()

    bread = Product(
        name="Bread",
        brand="Britannia",
        price=40,
        quantity=80,
        description="Whole wheat bread",
        category=categories["food"]
    )
    bread.save()

    phone = Product(
        name="Phone",
        brand="Samsung",
        price=15000,
        quantity=10,
        description="Android smartphone",
        category=categories["electronics"]
    )
    phone.save()

    loose_product = Product(
        name="Mystery Item",
        brand="Unknown",
        price=10,
        quantity=5,
        description="No category assigned",
        category=None
    )
    loose_product.save()

    return {
        "milk": milk,
        "bread": bread,
        "phone": phone,
        "loose_product": loose_product
    }


def seed_all():
    categories = seed_categories()
    products = seed_products(categories)

    return {
        "categories": categories,
        "products": products
    }


def clear_all():
    Product.objects.delete()
    ProductCategory.objects.delete()