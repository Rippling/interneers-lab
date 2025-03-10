from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.productsView),
    path('products/<int:id>/', views.productDetailView),
]