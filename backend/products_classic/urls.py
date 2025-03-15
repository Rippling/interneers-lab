from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_product),
    path('list/', views.get_products),
    path('<int:pk>/', views.get_product),
    path('<int:pk>/update/', views.update_product),
    path('<int:pk>/delete/', views.delete_product),
]
