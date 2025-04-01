from django.urls import path
from product.views.product_views import ProductController
from product.views.product_category_views import ProductCategoryView, SingleProductCategoryView

urlpatterns = [
    path("categories/", ProductCategoryView.as_view(), name="category_list"),
    path("categories/<str:category_id>/", SingleProductCategoryView.as_view(), name="category_detail"),
    path("", ProductController.as_view()),  
    path("<str:product_id>/", ProductController.as_view()),  
]
