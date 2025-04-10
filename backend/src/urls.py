from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from src.controllers.product_controller import product_endpoint
from src.controllers.product_category_controller import category_product_endpoint

def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('products', product_endpoint),
    path('products/<slug:request_id>', product_endpoint),
    path('categories/<slug:category_title>', category_product_endpoint),
]
