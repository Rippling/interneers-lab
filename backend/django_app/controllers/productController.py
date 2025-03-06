import json
from datetime import datetime
import math
from django.http import HttpRequest, JsonResponse

products= []

def productEndpoint(request: HttpRequest, request_id: int= 0):
    if request.method== "GET":
        return getProduct(request, request_id)
    if request.method== "POST":
        return addProduct(request)
    if request.method== "PATCH":
        return updateProduct(request, request_id)
    if request.method== "DELETE":
        return deleteProduct(request, request_id)
    else:
        error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": f"No endpoint for {request.method} request",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Check the documentation at https://github.com/Alph3ga/interneers-lab for the available API endpoints"
            })
        error_response.status_code= 400
        return error_response

def addProduct(request: HttpRequest):
    data= json.loads(request.body)
    validation= validate_product(data)

    if(not validation["valid"]):
        error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": validation["details"],
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": validation["suggestion"],
            })
        error_response.status_code= 400
        return error_response

    data["id"]= len(products)+1 
    products.append(data)

    response= JsonResponse(data)
    response.status_code= 201
    response.headers["Location"]= f"/products/{data["id"]}"  # Location of resource
    return response

def getProduct(request: HttpRequest, request_id: int):
    if(request_id!=0): # Reserve 0 id for collection requests
        index= findProduct(request_id)

        if(index== -1):
            error_response= JsonResponse({
                "code": "NOT_FOUND",
                "message": "The requested resource was not found",
                "details": f"Product with id {request_id} does not exist",
                "timestamp": f"{datetime.now()} GMT+0:00",
                "request": f"{request.method} {request.path}",
                "suggestion": "Use 'GET /products' to get a list of existing products with id",
                })
            error_response.status_code= 404
            return error_response

        return JsonResponse(products[index])
    
    return getProductPaginated(request)

def getProductPaginated(request: HttpRequest):
    start_id= int(request.GET.get("start", "1"))
    limit= int(request.GET.get("limit", "100"))

    start_index= findProduct(start_id)

    end_index= start_index+ limit if start_index+limit<len(products) else len(products)+1
    pages= math.ceil(len(products)/limit)

    prev_index= start_index- limit if start_index>=limit else 0

    response= JsonResponse({
        "data":products[start_index:end_index],
        "navigation":{
            "self": f"{request.path}/?start={start_id}&limit={limit}",
            "next": f"{request.path}/?start={products[end_index]["id"]}&limit={limit}" if end_index<len(products) else None,
            "prev": f"{request.path}/?start={products[prev_index]["id"]}&limit={limit}" if prev_index>-1 else None,
            "pages": pages,
            "current": math.ceil((start_index+1)/limit)
        }
    }, safe= False)
    response.status_code= 206  # Partial content
    return response


def updateProduct(request: HttpRequest, request_id: int):
    data= json.loads(request.body) 

    index= findProduct(request_id)
    if(index== -1):
        error_response= JsonResponse({
            "code": "NOT_FOUND",
            "message": "The requested resource was not found",
            "details": f"Product with id {request_id} does not exist",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Use 'GET /products' to get a list of existing products with id",
            })
        error_response.status_code= 404
        return error_response

    request_product= products[index]

    # Modify each key specified in the request 
    for key in data.keys():
        if(key=="id"):
            error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "Product ID cannot be updated",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Remove 'id' field from your request, or check if it matches the URI",
            })
        error_response.status_code= 404
        return error_response
        request_product[key]= data[key]
    
    response= JsonResponse({})
    response.headers["Location"]= f"/products/{request_id}"  # Location of resource
    response.status_code= 204  # No content in body
    return response

def deleteProduct(request: HttpRequest, request_id: int):
    index= findProduct(request_id)
    if(index== -1):
        error_response= JsonResponse({
            "code": "NOT_FOUND",
            "message": "The requested resource was not found",
            "details": f"Product with id {request_id} does not exist",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Use 'GET /products' to get a list of existing products with id",
            })
        error_response.status_code= 404
        return error_response
    products.pop(index)
    
    response= JsonResponse({})
    response.status_code= 204
    return response

def validate_product(data):
    if "name" not in data:
        return {
            "valid": False,
            "details": "'name' field is required for the product",
            "suggestion": "Re-send the request with an appropriate name field",
        }
    if type(data["name"]) is not str or len(data["name"])== 0:
        return {
            "valid": False,
            "details": "'name' field is invalid",
            "suggestion": "Re-send the request with an appropriate name field, it must be a non-empty string",
        }


    if "price" not in data:
        return {
            "valid": False,
            "details": "'price' field is required for the product",
            "suggestion": "Re-send the request with an appropriate price field (non-negative integer)",
        }
    if type(data["price"]) is not int or data["price"]< 0:
        return {
            "valid": False,
            "details": "'price' field is invalid",
            "suggestion": "Re-send the request with an appropriate price field, it must be a non-negative integer. \
            Check if you are sending a string instead",
        }

    if "quantity" not in data:
        return {
            "valid": False,
            "details": "'quantity' field is required for the product",
            "suggestion": "Re-send the request with an appropriate quantity field (non-negative integer)",
        }
    if type(data["quantity"]) is not int or data["quantity"]< 0:
        return {
            "valid": False,
            "details": "'quantity' field is invalid",
            "suggestion": "Re-send the request with an appropriate quantity field, it must be a non-negative integer. \
            Check if you are sending a string instead",
        }
    
    return { "valid": True}

def findProduct(request_id: int):
    # binary search through the products array

    l= 0
    r= len(products)
    
    while(l<r):
        mid= (l+r)//2
        if(products[mid]["id"]== request_id):
            return mid
        if(products[mid]["id"]< request_id):
            l= mid+1
        else:
            r= mid
    return -1