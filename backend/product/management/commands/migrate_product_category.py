#to run it, python manage.py migrate_products_category
from mongoengine.queryset.visitor import Q
from django.core.management.base import BaseCommand
from product.models.product import Product
from product.models.product_category import ProductCategory

class Command(BaseCommand):
    help = 'Migrate existing products by assigning a default category for products without one'

    def handle(self, *args, **options):
        default_category = ProductCategory.objects(title="Uncategorized").first()
        if not default_category:
            default_category = ProductCategory(
                title="Uncategorized",
                description="Products without a specific category"
            )
            default_category.save()        

        products_without_category = Product.objects(Q(category__exists=False) | Q(category=None))
        count=0
        for product in products_without_category:
            product.category = default_category
            product.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Migrated {count} products to 'Uncategorized' category."))