from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_world(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    name = request.GET.get("name","World")
    return JsonResponse({"message":f"Hello {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
]
