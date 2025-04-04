from django.core.management.base import BaseCommand
from products.models import Product, ProductCategory


class Command(BaseCommand):
    help = "Create product categories from existing product data"

    def handle(self, *args, **options):
        # Get all unique category strings from products
        categories = Product.objects.distinct("category")
        created_count = 0

        for cat_name in categories:
            if not cat_name:
                continue

            # Check if category exists
            if not ProductCategory.objects(title=cat_name).first():
                ProductCategory(title=cat_name).save()
                created_count += 1
                self.stdout.write(f"Created category: {cat_name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCreated {created_count} new categories from {len(categories)} unique values"
            )
        )
