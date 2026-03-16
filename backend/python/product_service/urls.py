from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_products, name="list_products"),
    path("create/", views.create_product, name="create_product"),
    path("<str:product_id>/", views.get_product , name="get_product"),
    path("delete/<str:product_id>/", views.delete_product, name="delete_product"),
    path("products-by-category/<str:category_id>/", views.list_products_by_category_id, name="list_products_by_category_id"),
    path("remove-category/<str:product_id>/", views.remove_category_from_product, name="remove_category_from_product"),
    path("add-category/<str:product_id>/<str:category_id>/", views.add_category_to_product, name="add_category_to_product"),
]