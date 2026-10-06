import sys
from django.apps import AppConfig
from django.core.management import call_command

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self):
        if 'runserver' not in sys.argv:
            return
        
        from .models import ProductCategory
        
        if ProductCategory.objects.count() == 0:
            print("Database is empty! Seeding default Product Categories...")
            
            default_categories = [
                ProductCategory(title="Food", description="Groceries and edible items"),
                ProductCategory(title="Kitchen Essentials", description="Cookware, utensils, and appliances"),
                ProductCategory(title="Electronics", description="Gadgets and tech accessories"),
                ProductCategory(title="Clothing", description="Apparel and wearables")
            ]
            
            ProductCategory.objects.insert(default_categories)
            
            print("Successfully seeded default categories!")