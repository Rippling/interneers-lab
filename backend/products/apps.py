from django.apps import AppConfig
from .connection import init_mongo


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        init_mongo()
