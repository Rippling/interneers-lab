from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from .views import create_product, get_product, list_products, update_product, delete_product

def hello_name(request):
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('hello/', hello_name),
    path('products/', list_products),
    path('products/create/', create_product,name="create_product"),
    path('products/<str:product_id>/', get_product),
    path('products/<str:product_id>/update/', update_product),
    path('products/<str:product_id>/delete/', delete_product),
]
