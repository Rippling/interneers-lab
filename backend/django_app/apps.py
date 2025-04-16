from django.apps import AppConfig
from django.db.utils import OperationalError
from django_app.models.category import Category

class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_app"

    def ready(self):
        from mongoengine.errors import NotUniqueError
        categories = [
            {"title": "Electronics", "description": "Electronic gadgets and devices"},
            {"title": "Clothing", "description": "Apparel and fashion wear"},
            {"title": "Books", "description": "Books from various genres"},
            {"title": "Food", "description": "Groceries and food items"},
            {"title": "Kitchen Essentials", "description": "Cookware and kitchen accessories"},
        ]
        try:
            for category in categories:
                if not Category.objects(title=category["title"]).first():
                    Category(**category).save()
        except (OperationalError, NotUniqueError) as e:
            print(f"Error seeding categories: {e}")