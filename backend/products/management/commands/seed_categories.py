from django.core.management.base import BaseCommand
from products.services.product_category_service import ProductCategoryService

DEFAULT_CATEGORIES = [
    {
        "title": "Healthcare",
        "description": "Medical supplies, wellness products, and personal care for physical and mental well-being.",
    },
    {
        "title": "Books",
        "description": "Fiction, non-fiction, educational, and professional books for all readers.",
    },
    {
        "title": "Sports",
        "description": "Sports equipment, activewear, and fitness gear for an active lifestyle.",
    },
    {
        "title": "Uncategorized",
        "description": "Default category for unclassified items.",
    },
]


class Command(BaseCommand):
    help = "Seed initial product categories using ProductCategoryService"

    def handle(self, *args, **options):
        service = ProductCategoryService()
        created_count = 0

        for category_data in DEFAULT_CATEGORIES:
            try:
                service.create_category(category_data)
                self.stdout.write(
                    self.style.SUCCESS(f"Created category: {category_data['title']}")
                )
                created_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Error creating '{category_data['title']}': {str(e)}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeding complete. {created_count}/{len(DEFAULT_CATEGORIES)} categories created"
            )
        )
