from django.urls import path
from .views import ProductController

urlpatterns = [
    path("", ProductController.as_view()),  
    path("<str:product_id>/", ProductController.as_view()),  
]
