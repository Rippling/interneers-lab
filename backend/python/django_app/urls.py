from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse
from django_app.adapters.api.views import hello_view 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_view),
    path('warehouse/', include("warehouse.urls")),
    path('product_service/', include("product_service.urls")),
]
