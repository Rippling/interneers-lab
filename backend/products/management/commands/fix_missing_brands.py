from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Assign default brand name to products with missing brand"
    
    def handle(self, *args, **options):
        default_brand_name = "Unknown"  
        
        updated = Product.objects.filter(brand__in=[None, '', ' ']).update(brand=default_brand_name)
        
        self.stdout.write(
            self.style.SUCCESS(f"Updated {updated} products with '{default_brand_name}' brand")
        )