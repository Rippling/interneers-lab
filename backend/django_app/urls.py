from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

from .controllers.product_controller import product_endpoint

def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('products', product_endpoint),
    path('products/<int:request_id>', product_endpoint),
]
