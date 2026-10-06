from django.http import JsonResponse
from django_app.application.greeter_service import greet


def hello_world(request):
    # url is /hello-world/?name="Kreesh" it returns Kreesh
    name = request.GET.get("name")
    message = greet(name)
    return JsonResponse({"message": message})
