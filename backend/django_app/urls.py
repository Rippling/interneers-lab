# django_app/urls.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name', default to 'World' if missing.
    """
    name = request.GET.get("username", "World")
    return JsonResponse({"message": f"Hello, {name}!"})

def new_fun_to_say_hello(request):
    """
    A view that returns 'Hello, {who}' in JSON format.
    Uses a query parameter named 'who', default to "Rippling"
    """
    company = request.GET.get("who", "Rippling")
    return JsonResponse({"company": f"Hello, {company}!"})

def gargi_s_function(request):
    """
    A view that returns a static message.
    """
    return JsonResponse({"My message": "Hello Django World, this is Gargi trying to learn Django"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    # Example usage: /hello/?username=Gargi
    # returns {"message": "Hello, Gargi!"}

    path('try/', new_fun_to_say_hello),
    # Example usage: /try/?who=new_company
    # returns {"company": "Hello, new_company!"}

    path('gargi/', gargi_s_function),
    # Example usage: /gargi/
]
