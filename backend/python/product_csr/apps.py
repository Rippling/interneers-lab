from django.apps import AppConfig


class ProductCsrConfig(AppConfig):
    name = "product_csr"

    def ready(self):
        from .services.category_service import CategoryService

        service = CategoryService()
        default_categories = ["Electronics", "Fashion", "Home"]

        for name in default_categories:
            service.create_category_if_not_exists(name)
