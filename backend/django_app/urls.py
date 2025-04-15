from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse,JsonResponse

'''

I attempted to use MongoDB and successfully created a collection and document. However, I encountered difficulties retrieving the data within my views function, likely due to data serialization issues. I plan to learn more about this and address it later

from django.conf import settings


users_collection=settings.MONGO_DB.Users


def get_user_data(name):
    user_data=users_collection.find_one({"name":name})
    if user_data:
        return user_data
    else:
        return None
'''

def hello_world(request):
    '''
    
    This is a simple view function that returns a JSON response with a message that includes the name, age, weight, height, and BMI of a person.
    The name, weight, and height are extracted from the query parameters of the request.
    The age is hardcoded to 20.'''


    name=request.GET.get("name","Ishamel")
    try:
        weight=float(request.GET.get("weight","48"))
        height=float(request.GET.get("height","1.5"))
        bmi=round(weight/height**2)
    except (ValueError, ZeroDivisionError):
        # Fetch user data from MongoDB if input is invalid

            return JsonResponse({"error": "Invalid input", "fun_fact": "Oops! Seems like you broke laws of physics. Please check your input and try again."}, status=400)

    
    return JsonResponse({"message":f"call me, {name}, iam 20 year old with {weight}kg and {height}m, my BMI is {bmi}"})

def home(request):
    '''
    This is home  page
    '''
    return HttpResponse("Hello,This is Earth")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('api/',include('products.urls')),

]
