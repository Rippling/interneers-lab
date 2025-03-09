# django_app/urls.py

from django.contrib import admin
from django.urls import path, include
from product.views import get_all_products

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", get_all_products, name="home"),
    path("product/", include("product.urls")),

]
