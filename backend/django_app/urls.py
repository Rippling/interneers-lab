from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.http import JsonResponse

import requests
import os
from dotenv import load_dotenv
load_dotenv()


# def hello_world(request):
#     return HttpResponse("Hello, world! This is our interneers-lab Django server.")

def hello_world(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    
    return JsonResponse({"message": f"Hello, {name}!"})
        
def get_current_weather(request):
    '''
    Uses query parameter named 'city' to get weather related information using OpenWeather's API.
    '''

    API_KEY = os.getenv("API_KEY")

    name = request.GET.get("name", "User")
    city = request.GET.get("city")

    if city == None:
        return JsonResponse({"message": f"Hello, {name}!"})

    request_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    weather_data = requests.get(request_url).json()

    if weather_data["cod"]!=200:
        '''
        User entered an invalid city name.
        '''

        return JsonResponse({"message": f"Hello, {name}! Please enter a valid city name."})
    
    temperature = weather_data["main"]["temp"]
    weather_description = weather_data["weather"][0]["description"]

    return JsonResponse({
            "message": f"Hello, {name}! Current temperature in {city} is {temperature}°C with {weather_description}."
        })
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('weather/', get_current_weather),
    path('api/', include('products.urls')),
]

