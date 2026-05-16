from django.urls import path, include
from django.http import JsonResponse


def hello_name(request):
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})


urlpatterns = [
    path("hello/", hello_name),
    path("", include("Product.urls")),
]