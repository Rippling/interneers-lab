from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse

def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server. And this app is running on my local machine..... Let's get started with the project.")

def is_valid_dob(dob):
    response = {
        "valid": True,
        "message": ""
    }

    try:
        date = int(dob[:2])
        month_index = int(dob[2:4])
        year = int(dob[4:])
        months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec']

        if month_index < 1 or month_index > 12:
            response["valid"] = False
            response["message"] = "Invalid date format: Month must be between 01 and 12 (MM). Please enter a valid month."
        elif month_index == 2 and date > 29:
            response["valid"] = False
            response["message"] = "Invalid date: February cannot have more than 29 days. Please enter a valid date."
        elif month_index == 2 and date == 29 and (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0)):
            response["valid"] = False
            response["message"] = f"Invalid date: {year} is not a leap year, so February has only 28 days."
        elif month_index in [1, 3, 5, 7, 8, 10, 12] and date > 31:
            response["valid"] = False
            response["message"] = f"Invalid date: {months[month_index - 1]} has only 31 days. Please enter a valid date."
        elif month_index in [4, 6, 9, 11] and date > 30:
            response["valid"] = False
            response["message"] = f"Invalid date: {months[month_index - 1]} has only 30 days. Please enter a valid date."
        else:
            response["message"] = f"I will surely wish you a very happy birthday on {date} {months[month_index-1]} every year."

    except ValueError:
        response["valid"] = False
        response["message"] = "Invalid input: DOB must be exactly 8 numeric digits (DDMMYYYY). Please enter a valid date."

    return response

def greet(request):
    name = request.GET.get("name", "World")
    dob = request.GET.get("dob")
    work_id = request.GET.get("workId", None)
    if not dob:
        return JsonResponse({
            "error": "dob is a required paramter in the format DDMMYYYY."
        })
    response = is_valid_dob(dob)

    if response["valid"]:
        return JsonResponse({
            "message": f"Hello {name}! {response['message']}",
            "work_id": work_id if work_id != None else "not assigned yet" 
        })
    else:
        return JsonResponse({"error": response["message"]})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('greet/', greet),
    path('inventory/', include("inventory.urls"))
]
