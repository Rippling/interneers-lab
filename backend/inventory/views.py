from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def hello(request):
    return HttpResponse("Hey! Welcome to the inventory application")