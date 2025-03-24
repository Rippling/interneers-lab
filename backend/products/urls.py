from django.urls import path

from .views.ProductView import (
    ProductCreate,
    ProductList,
    ProductDetail,
    ProductUpdate,
    ProductDelete,
    CheckCategoryView
)

from .views.CategoryView import CategoryView

urlpatterns = [
    path('products/create/', ProductCreate.as_view(), name='create-product'),
    path('products/', ProductList.as_view(), name='product-list'),  
    path('products/<str:id>/', ProductDetail.as_view(), name='product-detail'),  
    path('products/<str:id>/update/', ProductUpdate.as_view(), name='product-update'), 
    path('products/<str:id>/delete/', ProductDelete.as_view(), name='product-delete'),  
    path("check-category/", CheckCategoryView.as_view(), name="check_category"),
    path('categories/', CategoryView.as_view(), name='category-list'),
    path('categories/<str:title>/', CategoryView.as_view(), name='category-detail'),
    # path('/products/<str:product_id>/add-to-category/' , )
]
