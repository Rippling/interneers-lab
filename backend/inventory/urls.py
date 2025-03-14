from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from . import views


urlpatterns = [
    path('products', views.get_all_products, name = "getall-products"),
    path('products/page/<int:page_no>', views.get_products, name = "products_page"),
    path('products/create', views.create_product, name = "create-product"),
    path('products/<int:id>', views.update_product, name="update-product")
]