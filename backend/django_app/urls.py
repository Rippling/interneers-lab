from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.http import JsonResponse

# def hello_world(request):
#     return HttpResponse("Hello, world! This is our interneers-lab Django server.")

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('hello/', hello_world),
# ]


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
    path('hello_name/', hello_name),    #test this using -> http://127.0.0.1:8001/hello_name/?name=Vedanshi
]