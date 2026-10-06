# django_app/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    
]