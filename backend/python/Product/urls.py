from django.urls import path
from .controller.views import (
    ProductListView,
    ProductDetailView,
    ProductBulkView,
    ProductCategoryMembershipView,
    ProductCategoryListView,
    ProductCategoryDetailView,
    ProductsByCategoryView,
)

urlpatterns = [
    path("categories/", ProductCategoryListView.as_view()),
    path("categories/<str:category_id>/", ProductCategoryDetailView.as_view()),
    path("categories/<str:category_id>/products/", ProductsByCategoryView.as_view()),
    path("products/", ProductListView.as_view()),
    path("products/bulk/", ProductBulkView.as_view()),
    path("products/<str:product_id>/", ProductDetailView.as_view()),
    path(
        "products/<str:product_id>/category/", ProductCategoryMembershipView.as_view()
    ),
]
