# to run these commands, use'python manage.py fix_missing_brands'
from django.core.management import BaseCommand
from product.models.product import Product
from mongoengine.queryset.visitor import Q

class Command(BaseCommand):
    help = 'Update existing products without a brand to have a default brand'

    def handle(self, *args, **options):
        default_brand = "Unknown Brand"
        products = Product.objects(Q(brand__exists=False)|Q(brand=''))
        count = 0
        for product in products:
            product.brand = default_brand
            product.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {count} products with a default brand."))