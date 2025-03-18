from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from . import views, controllers


urlpatterns = [
    # path('products', views.get_all_products, name = "getall-products"),
    # path('products/page/<int:page_no>', views.get_products, name = "products_page"),
    # path('products/create', views.create_product, name = "create-product"),
    # path('products/<int:id>', views.update_product, name="update-product"),
    
    path('products', controllers.get_all_products, name = "getall-products"),
    path('products/create', controllers.create_product, name = "create-product"),
    path('products/<str:id>', controllers.get_product_by_id, name="get_product_by_id"),
    path('products/<str:id>/update', controllers.update_product, name="update-product"),
    path('products/<str:id>/delete', controllers.delete_product, name="delete-product")
]