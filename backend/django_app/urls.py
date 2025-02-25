from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.http import JsonResponse

# def hello_world(request):
#     return HttpResponse("Hello, world! This is our interneers-lab Django server.I have started my interneers lab on 24th Feb.")

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('hello/', hello_world),
# ]

def hello_name(request):
    """
    A simple view that returns 'Hello, I am {name}.I am {age} years old!' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    age = request.GET.get("age", "unknown") 

    return JsonResponse({"message": f"Hello, I am {name}.I am {age} years old!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    # Example usage: /hello/?name=Bob&age=25
    # returns {"message": "Hello, I am Bob.I am 25 years old!"}
]
