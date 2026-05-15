# django_app/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
    # Example usage: /hello/?name=Bob
    # returns {"message": "Hello, Bob!"}
    path("", include("django_app.adapters.api.urls")),
    path("week2/", include("week2.urls")),
    path("week3/", include("week3.urls")),
    path("week4/", include("week4.urls")),

]
