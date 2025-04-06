from django.core.management.base import BaseCommand
from ..models.ProductModel import Product

class Command(BaseCommand):
    help='Add a default brand to products without a brand'

    def handle(self, *args, **kwargs):
        prod_without_brand=Product.objects.filter(brand__in=[None, ''])

        count = 0

        for product in prod_without_brand:
            try:
                product.brand='Unknown'
                product.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'Updated product {product.id} with default brand'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error updating product {product.id}: {str(e)}'))

