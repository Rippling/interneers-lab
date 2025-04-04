from django.urls import path
from .views import ProductView, ProductCategoryView

urlpatterns = [
    path('products/', ProductView.as_view(), name='product_list'),
    path('products/<str:product_id>/', ProductView.as_view(), name='product_detail'),
    path("products/category/<str:category_id>/", ProductView.as_view(), name="product-category"),  # By categor
    path('products/<str:product_id>/category/<str:category_id>/', ProductView.as_view(), name='assign_product_to_category'),
    path('products/<str:product_id>/category/remove/', ProductView.as_view(), name='remove_product_from_category'),
    # Product Category Endpoints
    path('categories/', ProductCategoryView.as_view(), name='category_list'),
    path('categories/<str:category_id>/', ProductCategoryView.as_view(), name='category_detail'),
]

