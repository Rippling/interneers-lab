from django.core.management.base import BaseCommand
from product_csr.seed import clear_product_csr_data, seed_product_csr_data


class Command(BaseCommand):
    help = "Seed product_csr sample data"

    def handle(self, *args, **options):
        clear_product_csr_data()
        seed_product_csr_data()
        self.stdout.write(self.style.SUCCESS("product_csr data seeded successfully"))
