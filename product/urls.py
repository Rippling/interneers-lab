from django.urls import path
from .views import ProductListView,ProductDetailView,RecentUpdatedProductsView,ProductHistoryView
# from .views import ProductAPI

# urlpatterns = [
#     path('products/', ProductAPI.as_view(), name='product-list'),
#     path('products/<int:product_id>/', ProductAPI.as_view(), name='product-detail'),
# ]


urlpatterns = [
    path('products/',ProductListView.as_view(),name='product-list'),
    path('products/<str:prod_id>/',ProductDetailView.as_view(),name='product-detail'),
    path('recent-updates/',RecentUpdatedProductsView.as_view(),name='recent-updates'),
    path('product-history/<str:prod_id>/',ProductHistoryView.as_view(),name='product-history')
]
