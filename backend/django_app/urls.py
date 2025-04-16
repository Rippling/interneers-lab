from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.http import JsonResponse

# def hello_world(request):
#     return HttpResponse("Hello, world! This is our interneers-lab Django server.")

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('hello/', hello_world),
# ]


def home(request):
    return HttpResponse("Hi")


def hello(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server, First change made, function name changed from i.e hello_world to hello")

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
    path('hello/', hello),
    path('', home),
    path('hello_name/', hello_name),    #test this using -> hello_name/?name=Vedanshi
    #tested with few more apis like http://127.0.0.1:8000/hello_name/?name=John%20Doe!@#   , etc
   path('api/', include('products.urls')), 
]
