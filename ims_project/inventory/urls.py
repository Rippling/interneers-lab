from django.urls import path
from .views import ProductView, ProductCategoryView

product_views = ProductView()
category_views = ProductCategoryView()


urlpatterns = [
    path('products/', product_views.product_collection_view, name='product_collection'),

    path('products/<str:product_id>/', product_views.product_detail_view, name='product_detail'),

    path('categories/', category_views.category_collection_view, name='category_collection'),

    path('categories/<str:title>/', category_views.category_detail_view, name='category_detail'),
]