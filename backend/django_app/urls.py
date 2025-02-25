from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.http import JsonResponse

def hello_name(request):
    """
    A simple view that returns 'Hello, I am {name}.I am {age} years old! I am from {city}.' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "unknown")
    age = request.GET.get("age", "unknown") 
    city = request.GET.get("city", None)

    response_data = {
        "message": f"Hello, I am {name}. I am {age} years old!"
    }

    if city:
        response_data["city_info"] = f"I am from {city}."

    return JsonResponse(response_data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    # Example usage: /hello/?name=Bob&age=25&city=NewYork
    # returns {"message": "Hello, I am Bob.I am 25 years old! I am from New York."}
]
