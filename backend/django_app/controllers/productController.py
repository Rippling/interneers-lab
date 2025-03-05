from django.http import HttpResponse, HttpRequest, JsonResponse
import json

products= []

def productEndpoint(request: HttpRequest, request_id: int= 0):
    if request.method== "GET":
        return getProduct(request, request_id)
    if request.method== "POST":
        return addProduct(request)
    if request.method== "PATCH":
        return updateProduct(request, request_id)
    else:
        error_response= JsonResponse({"message": f"No endpoint for {request.method} request"})
        error_response.status_code= 400
        return error_response

def addProduct(request: HttpRequest):
    data= json.loads(request.body)
    data["id"]= len(products)+1 
    products.append(data)

    response= JsonResponse(data)
    response.status_code= 201
    response.headers["Location"]= f"/products/{data["id"]}"  # Location of resource
    return response

def getProduct(request: HttpRequest, request_id: int):
    if(request_id!=0): # Reserve 0 id for collection requests
        return JsonResponse(products[request_id-1])
    return JsonResponse(products, safe= False)

def updateProduct(request: HttpRequest, request_id: int):
    data= json.loads(request.body) 
    request_product= products[request_id]

    # Modify each key specified in the request 
    for key in data.keys():
        request_product[key]= data[key]
    
    response= JsonResponse({})
    response.headers["Location"]= f"/products/{request_id}"  # Location of resource
    response.status_code= 204  # No content in body
    return response