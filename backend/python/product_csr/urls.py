from django.urls import path 
from . import views


urlpatterns = [
    path('products/',views.products),
    path('products/bulk-upload/', views.bulk_upload_product),
    path('products/<str:product_id>/', views.product_detail),
    path('categories/', views.categories),
    path('categories/<str:category_id>/',views. category_detail),
    path('categories/<str:category_id>/products/', views.category_products),
    path('categories/<str:category_id>/add-product/', views.add_product_to_category),
    path('categories/<str:category_id>/remove-product/', views.remove_product_from_category),
]

