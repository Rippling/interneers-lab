from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_product_categories , name="get_all_product_categories"),
    path("create/", views.create_product_category , name="create_product_category"),
    path("<str:product_category_id>/", views.get_product_category_by_id, name="get_product_category_by_id"),
    path("update/<str:product_category_id>/", views.update_product_category, name="update_product_category"),
    path("delete/<str:product_category_id>/", views.delete_product_category, name="delete_product_category"),
]
