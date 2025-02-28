# django_app/urls.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'username' from the query string, default to 'World' if missing
    name = request.GET.get("username", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

    # Get 'who' from the query string, default to 'Rippling' if missing
def new_fun_to_say_hello(request):
    company = request.GET.get("who", "Rippling")
    return JsonResponse({"company": f"Hello, {company}!"})

def gargi_s_function(request):
    return JsonResponse({"My message":"Hello Django World, this is Gargi trying to learn Django"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    # Example usage: /hello/?username = Gargi
    # returns {"message": "Hello, Gargi!"}
    path('try/', new_fun_to_say_hello),
    # Example usage: /try/?who = new_company
    # returns {"message": "Hello, new_company!"}
    path('gargi/', gargi_s_function),
     # Example usage: /gargi/ 
]
