import json

from src.services.product_category_service import ProductCategoryService
from mongoengine.errors import DoesNotExist

def initialize_categories():
    with open("PRODUCT_CATEGORIES.json","r") as json_file:
        categories= json.load(json_file)
        for category in categories:
            try:
                ProductCategoryService.get_category_by_title(category["title"])
            except DoesNotExist:
                ProductCategoryService.create_category(category["title"], category["description"])

if __name__== "__main__":
    initialize_categories()