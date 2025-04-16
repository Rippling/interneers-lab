# django_app/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import routers
from django_app.views.product_views import ProductViewSet
from django_app.views.category_views import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    age = request.GET.get("age", "unknown")
    location = request.GET.get("location", "somewhere")
    # Age validation
    if age is not None:
        try:
            age = int(age)
            if age < 0:
                return JsonResponse({"error": "Age cannot be negative."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Age must be an integer."}, status=400)
    else:
        age = "unknown"
    return JsonResponse({
        "message": f"Hello, {name}!",
        "details": {
            "age": age,
            "location": location
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    # Example usage: /hello/?name=Bob
    # returns {"message": "Hello, Bob!"}
    path('', include(router.urls)),
    path(
        'categories/<str:pk>/products/',
        CategoryViewSet.as_view({'get': 'list_products'}),
        name='category-products'
    ),
    path(
        'categories/<str:pk>/add_product/',
        CategoryViewSet.as_view({'post': 'add_product'}),
        name='category-add-product'
    ),
    path(
        'categories/<str:pk>/remove_product/<str:product_id>/',
        CategoryViewSet.as_view({'delete': 'remove_product'}),
        name='category-remove-product'
    ),
]
