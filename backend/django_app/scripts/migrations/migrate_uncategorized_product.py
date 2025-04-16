import sys
import os
from django.utils import timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")

import django
django.setup()

from django_app.models.product import Product
from django_app.models.category import Category

def migrate_uncategorized_products():
    uncategorized = Category.objects(title="Uncategorized").first()
    if not uncategorized:
        uncategorized = Category(
            title="Uncategorized",
            description="Default category for old products"
        )
        uncategorized.save()

    uncategorized_products = Product.objects(category=None)

    count = 0
    for product in uncategorized_products:
        product.category = uncategorized
        product.updated_at = timezone.now()
        product.save()
        count += 1

    print(f"Migrated {count} old products to 'Uncategorized' category")

if __name__ == "__main__":
    migrate_uncategorized_products()
