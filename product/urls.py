from django.urls import path
from .views import ProductAPI

urlpatterns = [
    path('products/', ProductAPI.as_view(), name='product-list'),
    path('products/<int:product_id>/', ProductAPI.as_view(), name='product-detail'),
]
