from django.urls import path
from .views.ProductView import ProductListView,ProductDetailView,RecentUpdatedProductsView,ProductHistoryView
from .views.CategoryView import (
    ProdCategoryListView, 
    ProdCategoryDetailView, 
    CategoryProductsView,
    ProdCategoryManagementView
)

# from .views import ProductAPI

# urlpatterns = [
#     path('products/', ProductAPI.as_view(), name='product-list'),
#     path('products/<int:product_id>/', ProductAPI.as_view(), name='product-detail'),
# ]


urlpatterns = [
    path('products/',ProductListView.as_view(),name='product-list'),
    path('products/<str:prod_id>/',ProductDetailView.as_view(),name='product-detail'),
    path('recent-updates/',RecentUpdatedProductsView.as_view(),name='recent-updates'),
    path('product-history/<str:prod_id>/',ProductHistoryView.as_view(),name='product-history'),
    path('categories/',ProdCategoryListView.as_view(),name='category-list'),
    path('categories/id/<str:category_id>/',ProdCategoryDetailView.as_view(),name='category-detail'),
    path('categories/title/<str:title>/',ProdCategoryDetailView.as_view(),name='category-search'),
    path('categories/<str:category_id>/products/',CategoryProductsView.as_view(),name='category-products'),
    path('prod-categories/manage-products/',ProdCategoryManagementView.as_view(),name='category-product-management'),   
]
