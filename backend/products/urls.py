from django.urls import path

from .views.ProductView import (
    ProductCreate,
    ProductList,
    ProductDetail,
    ProductUpdate,
    ProductDelete,
    # CheckCategoryView,
    AddCategoryToProduct,
    RemoveCategoryFromProduct,
    
)

from .views.CategoryView import (CategoryView , CategoryDetail, CategoryList)

urlpatterns = [
    path('products/create/', ProductCreate.as_view(), name='create-product'),
    path('products/', ProductList.as_view(), name='product-list'),  
    path('products/<str:id>/', ProductDetail.as_view(), name='product-detail'),  
    path('products/<str:id>/update/', ProductUpdate.as_view(), name='product-update'), 
    path('products/<str:id>/delete/', ProductDelete.as_view(), name='product-delete'),  
    # path("check-category/", CheckCategoryView.as_view(), name="check_category"),
    path('categories/', CategoryView.as_view(), name='category-create'),
    path('categories/all', CategoryList.as_view(), name='category-list'),
    path('categories/<str:title>/update', CategoryView.as_view(), name='category-update'),      
    path('categories/title/<str:title>/', CategoryView.as_view(), name='category-title-detail'),
    path('categories/id/<str:id>/', CategoryDetail.as_view(), name='category-id-detail'),      
    path('products/<str:product_id>/add-category/<str:category_id>/', AddCategoryToProduct.as_view(), name='add_category_to_product'),
    path('products/<str:product_id>/remove-category/<str:category_id>/', RemoveCategoryFromProduct.as_view(), name='remove_category_from_product'),
    
]
