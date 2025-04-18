from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse

def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server. Making changes0...")

def hello_name(request):
    name=request.GET.get("name", "World")
    # return HttpResponse(f"Hello, {name}!")
    return JsonResponse({"message":f"Hello, {name}!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('hello/', hello_name),
]
