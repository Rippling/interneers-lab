from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('warehouse/', include("warehouse.urls")),
    path('product_service/', include("product_service.urls")),
    path('product_category/', include("product_category.urls")),
]
