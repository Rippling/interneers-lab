from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def hello_name(request):
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

def hello_details(request):
    # Get parameters with default values if not provided
    name = request.GET.get("name", "World")
    age = request.GET.get("age", None)
    city = request.GET.get("city", None)
    
    # Construct the message based on parameters
    message = f"Hello, {name}!"
    
    if age:
        message += f" You are {age} years old."
    if city:
        message += f" You're from {city}."
    
    return JsonResponse({"message": message})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
    path('details/', hello_details),
    path('api/drf', include('products.urls')),
    path('api/classic/', include('products_classic.urls')),
]
