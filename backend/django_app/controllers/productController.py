from django.http import HttpResponse, HttpRequest
import json

products= []

def addProduct(request: HttpRequest):
    data= json.loads(request.POST) 
    print(request.body)
    return HttpResponse("Added Product")