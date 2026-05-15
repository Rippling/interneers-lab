from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailAPIView, ProductCategoryDetailAPIView, ProductCategoryListCreateAPIView, CategoryProductsAPIView, AddProductToCategoryAPIView, RemoveProductFromCategoryAPIView, BulkProductUploadAPIView


urlpatterns = [
    # CRUD product
    path("products/", ProductListCreateAPIView.as_view(),
         name="product-list-create"),
    path("products/<int:id>/", ProductDetailAPIView.as_view(), name="product-detail"),
    # CRUD category
    path("categories/", ProductCategoryListCreateAPIView.as_view(),
         name="category-list-create"),
    path("categories/<int:id>/", ProductCategoryDetailAPIView.as_view(),
         name="category-detail"),
    # products belonging to same category
    path("categories/<int:category_id>/products/",
         CategoryProductsAPIView.as_view(), name="category-products"),
    # add or remove products from category
    path("categories/<int:category_id>/add-product/",
         AddProductToCategoryAPIView.as_view(), name="add-product-to-category"),
    path("categories/<int:category_id>/remove-product/",
         RemoveProductFromCategoryAPIView.as_view(), name="remove-product-from-category"),
    # csv upload
    path("products/bulk-upload/", BulkProductUploadAPIView.as_view(),
         name="product-bulk-upload")
]
