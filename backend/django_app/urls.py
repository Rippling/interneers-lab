from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

urlpatterns = [
    path('hello/', hello_name),
]
