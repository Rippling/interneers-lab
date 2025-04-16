from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.conf.urls.static import static
from django.conf import settings  # Import settings here

from products.views1 import show_product_page , product_detail_view , show_categories_page, category_detail_view

urlpatterns = [
    path('api/', include('products.urls')), 
    path('products/page/', show_product_page, name='product_page'),
    path('products/<str:id>/', product_detail_view, name='product-detail'),
    path('categories/page/', show_categories_page, name='category_page'),
    path('categories/title/<str:title>', category_detail_view, name='category-detail-products'),
] 