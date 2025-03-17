from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.productsView),
    path('products/<str:id>/', views.productDetailView), # id changed to str
]