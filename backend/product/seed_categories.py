from product.models.product_category import ProductCategory

def seed_categories():
    default_categories = [
        {"title": "Food", "description": "Edible items and groceries"},
        {"title": "Kitchen Essentials", "description": "Utensils and Kitchen tools"},
        {"title": "Electronics", "description": "Electronic devices and appliances"},
    ]

    for cat in default_categories:
        if not ProductCategory.objects(title=cat["title"]).first():
            ProductCategory(**cat).save()

    print("Product categories seeded succeessfully.") 