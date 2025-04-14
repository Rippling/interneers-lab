from django.urls import path
from products.controllers.product_controller import productsView, productDetailView
from products.controllers.product_category_controller import (
    productCategoryView,
    productCategoryDetailView,
)

urlpatterns = [
    path("products/", productsView , name='products'),
    path("products/<str:id>/", productDetailView, name='product-detail'),
    path("categories/", productCategoryView, name='product-categories'),
    path("categories/<str:id>/", productCategoryDetailView, name='product-category-detail'),
]
