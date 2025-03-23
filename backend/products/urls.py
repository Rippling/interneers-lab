from django.urls import path
from products.controllers.product_controller import productsView, productDetailView

urlpatterns = [
    path('products/', productsView),
    path('products/<str:id>/', productDetailView), # id changed to str
]