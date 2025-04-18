from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.controllers.product import ProductViewSet
from product.controllers.product_category import ProductCategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', ProductCategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls))
]
# urlpatterns=[
#     path('products/', product.get_all_products, name='get_all_products'),
#     path('products/create/', product.create_product, name='create_product'),
#     path('products/update/<str:product_id>/', product.update_product, name='update_product'),
#     path('products/delete/<str:product_id>/', product.delete_product, name='delete_product'),
#     path('products/<str:product_id>/', product.get_product, name='get_product'),
# ]