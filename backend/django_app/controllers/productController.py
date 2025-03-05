from django.http import HttpResponse, HttpRequest, JsonResponse
import json

products= []

def addProduct(request: HttpRequest):
    data= json.loads(request.body)
    data["id"]= len(products) 
    products.append(data)
    response= {
        "id": data["id"],
    }
    return JsonResponse(response)

def getProduct(request: HttpRequest):
    request_id= int(request.GET.get("id", "0"))
    if(request_id!=0): 
        return JsonResponse(products[request_id])
    return JsonResponse(products, safe= False)

def updateProduct(request: HttpRequest):
    data= json.loads(request.body) 
    request_id= data["id"]
    request_product= products[request_id]
    for key in data.keys():
        request_product[key]= data[key]
    return JsonResponse(products[request_id])