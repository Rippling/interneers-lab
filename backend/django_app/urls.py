from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .product_api import ProductAPIView


def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('products/', ProductAPIView.as_view(), name='products'),
]
