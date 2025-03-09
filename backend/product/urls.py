from django.urls import path
from .views import create_product, get_all_products, get_product, update_product, delete_product

urlpatterns = [
    path("", get_all_products, name="api_home"),  
    path("create/", create_product, name="create_product"),
    path("get_all/", get_all_products, name="get_all_products"),
    path("get/<int:product_id>/", get_product, name="get_product"),
    path("update/<int:product_id>/", update_product, name="update_product"),
    path("delete/<int:product_id>/", delete_product, name="delete_product"),
    
]
