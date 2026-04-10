from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.product_list_controller, name="product-list"),
    path('categories/', views.category_list_controller, name='category-list'),
    path('categories/<str:category_id>/products/', views.category_products_controller, name='category-products'),
    path('products/bulk/',views.bulk_create_products,name='bulk-create'),
    path('products/<str:product_id>/', views.product_detail_controller, name='product-detail'),
    
]