from django.http import HttpResponse, HttpRequest, JsonResponse
import json

products= []

def productEndpoint(request: HttpRequest, request_id: int= 0):
    if request.method== "GET":
        return getProduct(request, request_id)
    if request.method== "POST":
        return addProduct(request)
    if request.method== "PATCH":
        return updateProduct(request)
    else:
        error_response= JsonResponse({"message": f"No endpoint for {request.method} request"})
        error_response.status_code= 400
        return error_response

def addProduct(request: HttpRequest):
    data= json.loads(request.body)
    data["id"]= len(products)+1 
    products.append(data)
    response= {
        "id": data["id"],
    }
    return JsonResponse(response)

def getProduct(request: HttpRequest, request_id: int):
    if(request_id!=0): 
        return JsonResponse(products[request_id-1])
    return JsonResponse(products, safe= False)

def updateProduct(request: HttpRequest):
    data= json.loads(request.body) 
    request_id= data["id"]
    request_product= products[request_id]
    for key in data.keys():
        request_product[key]= data[key]
    return JsonResponse(products[request_id])