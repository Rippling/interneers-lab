from products.models import Product
from django.core.management.base import BaseCommand 

class Command(BaseCommand):
    help = "Migrate brands from old format to new format"

    def handle(self, *args, **options):
        products = Product.objects()
        for product in products:
            if not product.brand or product.brand.strip() == "":
              product.brand = "Unknown"
              product.save()

        self.stdout.write(self.style.SUCCESS("Successfully migrated brands for all products"))
          