from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),
]
