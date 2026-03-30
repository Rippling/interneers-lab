from django.urls import path
from .views import ProductListCreateAPI, ProductDetailAPI

urlpatterns = [
    path('products/', ProductListCreateAPI.as_view()),
    # We use <int:pk> because the database automatically assigns an integer ID (Primary Key)
    path('products/<int:pk>/', ProductDetailAPI.as_view()), 
] 