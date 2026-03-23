from django.apps import AppConfig


class ProductapiConfig(AppConfig):
    name = 'productAPI'
    
    # def ready(self):
    #     try:
    #         from productAPI.seed.category_seed import seed_categories
    #         seed_categories()
    #     except Exception as e:
    #         print(f"[Seed] Warning: {e}")
