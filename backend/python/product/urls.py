from django.urls import path 
from . import views


urlpatterns = [
    path("products/",views.create_product),
    path("products/<int:id>/",views.get_product),
    path("products/<int:id>/update/",views.update_product),
    path("products/<int:id>/delete/",views.delete_product),
]
