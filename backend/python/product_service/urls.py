from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_products),
    path("create/", views.create_product),
    path("<str:product_id>/", views.get_product),
    path("delete/<str:product_id>/", views.delete_product),
]