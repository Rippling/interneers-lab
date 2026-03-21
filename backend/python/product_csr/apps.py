from django.apps import AppConfig


class ProductCsrConfig(AppConfig):
    name = 'product_csr'

    def ready(self):
        from .services.category_service import create_category_if_not_exists

        default_categories = ["Electronics", "Fashion", "Home"]

        for name in default_categories:
            create_category_if_not_exists(name)