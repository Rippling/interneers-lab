from django.urls import path,include
# from rest_framework import viewsets
# from rest_framework.routers import DefaultRouter
from .views import ProductView,ProductDetailView,ProductCategoryView,ProductsByCategoryView


# router=DefaultRouter()
# router.register(r'products',ProductViewSet,basename='products')
urlpatterns = [
    # path('',include(router.urls))
    path('list',ProductView.as_view(),name='product-list'),
    path('list/<int:product_id>',ProductDetailView.as_view(),name='product-detail'),
    path('category/list',ProductCategoryView.as_view(),name='product-category'),
    # path('category/list/<int:category_id>',ProductCategoryView.as_view(),name='product-category'),
    path('category/<int:category_id>/products', ProductsByCategoryView.as_view(), name='products-by-category'),

]

