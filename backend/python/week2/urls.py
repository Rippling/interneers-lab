from django.urls import path

from .views import ProductDetailAPIView, ProductListCreateAPIView

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(),
         name="product-list-create"),
    path("products/<int:product_id>/",
         ProductDetailAPIView.as_view(), name="product-detail"),
]
