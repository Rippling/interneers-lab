from django.urls import path
from .views import (
    create_category, get_category, list_categories, update_category, delete_category,
    create_product, get_product, list_products, list_products_by_category, update_product, delete_product
)

urlpatterns = [
    # ProductCategory APIs
    path('categories/', list_categories),
    path('categories/create/', create_category),
    path('categories/<str:category_id>/', get_category),
    path('categories/<str:category_id>/update/', update_category),
    path('categories/<str:category_id>/delete/', delete_category),

    # Product APIs
    path('products/', list_products),
    path('products/create/', create_product),
    path('products/<str:product_id>/', get_product),
    path('products/<str:product_id>/update/', update_product),
    path('products/<str:product_id>/delete/', delete_product),
    path('products/category/<str:category_title>/', list_products_by_category),
]
