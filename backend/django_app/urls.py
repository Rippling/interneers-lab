from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse

def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server. And this app is running in my local machine..... Let's get started with the project.")

def hello_name(request):
    name = request.GET.get("name", "World") # default will be World if value for name is not found
    data = {
        "message": f"Hello {name} !" 
    }
    return JsonResponse(data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('hello_name/', hello_name)
]
