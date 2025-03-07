# django_app/urls.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format with age and location.
    
    - Uses query parameters:
        - 'username' → The user's name (default: 'World' if missing).
        - 'location' → The user's location (default: 'Unknown' if missing).
        - 'age' → The user's age (default: 'N/A' if missing).
    
    - Handles edge cases:
        1. If 'age' is provided but is not a number, an error message is returned.
        2. If any parameter is missing, default values are used.
        3. Returns a JSON response with a formatted greeting.
    """
    # Get query parameters with default values if missing
    name = request.GET.get("username", "World")
    location = request.GET.get("location", "Unknown")
    age = request.GET.get("age", "N/A")

    if age != "N/A" and not age.isdigit():
        return JsonResponse({"error": "Invalid age. It must be a number."})
    if age < 0 and not age.isdigit():
        return JsonResponse({"error": "Invalid age. It must be a number."})


    return JsonResponse({
        "message": f"Hello, {name}!",
        "location": f"Your location is {location}.",
        "age": f"Your age is {age}."
    })

def new_fun_to_say_hello(request):
    """
    A view that returns 'Hello, {who}' in JSON format.
    Uses a query parameter named 'who', default to "Rippling"
    """
    id = request.GET.get("id", "N/A")
    company = request.GET.get("who", "Rippling")
    return JsonResponse({"company": f"Hello, {company} with id {id}!"})

def gargi_s_function(request):
    """
    A view that returns a static message.
    """
    return JsonResponse({"My message": "Hello Django World, this is Gargi trying to learn Django"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name), 
    path('hello/', hello_name), 
    # Example: /hello/?username=Gargi&location=India&age=20
    # Response: {"message": "Hello, Gargi.\n Your location is India.\n Your age is 20!"}
    # Invalid age (e.g., age=abc): {"error": "Invalid age. It must be a number."}
    # Missing params: Defaults to "World", "Unknown", "N/A"

    path('try/', new_fun_to_say_hello),
    # Example usage: /try/?who=new_company
    # returns {"company": "Hello, new_company!"}

    path('gargi/', gargi_s_function),
    # Example usage: /gargi/
]
