from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Copy product.category to product.old_category and delete category'

    def handle(self, *args, **options):
        
        products = Product.objects(category__exists=True)
        
        updated_count = 0
        for product in products:
            
            product.old_category = product.category
            
            del product.category  
            product.save()
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully migrated {updated_count} product categories to old_category and removed category')
        )