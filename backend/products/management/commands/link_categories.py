# products/management/commands/link_from_old_category.py
from django.core.management.base import BaseCommand
from products.models import Product, ProductCategory

class Command(BaseCommand):
    help = 'Link products to categories using old_category data and clean up old fields'

    def handle(self, *args, **options):
        
        products = Product.objects(old_category__exists=True)
        
        updated_count = 0
        cleaned_count = 0
        skipped = []
        
        for product in products:
            
            category_name = product.old_category
            
            
            category = ProductCategory.objects(title=category_name).first()
            
            if category:
                product.category = category  
                updated_count += 1
                
            else:
                skipped.append(category_name)

            
            if hasattr(product, 'old_category'):
                del product.old_category
            if hasattr(product, 'category_ref'):
                del product.category_ref
            
            product.save()
            cleaned_count += 1

        # Output results
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully linked {updated_count} products and cleaned {cleaned_count} records'
            )
        )
        
        if skipped:
            unique_skipped = set(skipped)
            self.stdout.write(
                self.style.WARNING('\nCategories not found for:')
            )
            for name in unique_skipped:
                self.stdout.write(f'- {name}')