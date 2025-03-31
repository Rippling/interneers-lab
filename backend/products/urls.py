from django.urls import path,include
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet


router=DefaultRouter()
router.register(r'products',ProductViewSet,basename='products')
urlpatterns = [
    path('',include(router.urls))
]
