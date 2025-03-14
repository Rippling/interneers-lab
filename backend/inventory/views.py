from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .ram import PRODUCTS
import json


# Create your views here.
def hello(request):
    return HttpResponse("Hey! Welcome to the inventory application")

def get_all_products(request):
    if request.method == "GET":
        print("ITS A GET REQUEST !!!")
        products = PRODUCTS
        print(products)
        return JsonResponse({
            "Products" : products
        })

    else:
        return JsonResponse({
            "error": f"Invalid Request"
        })
    

def get_products(request, page_no):
    if request.method == "GET":
        print(f"ITS A GET REQUEST FOR PAGE {page_no} !!!")
        start_index= max(0, 5 * page_no)
        end_index = min(start_index + 5, len(PRODUCTS.keys()))
        product_keys = list(PRODUCTS.keys())[start_index:end_index]
        # print(product_keys)
        products = {}
        for key in product_keys:
            products[key] = PRODUCTS[key]
        return JsonResponse({
            "Page" : page_no,
            "Products" : products
        })

    else:
        return JsonResponse({
            "error": f"Invalid Request"
        })


@csrf_exempt
def create_product(request):
    if request.method == "POST":
        print("POST REQUEST")
        data = json.loads(request.body.decode("utf-8"))
        product = {}
        for key in data:
            # print(key)
            product[key] = data[key]
        product['id'] = len(PRODUCTS.keys())
        PRODUCTS[product['id']] = product

        return JsonResponse({
            "message" : f"Product created successfully",
            "product id" : f"{product['id']}"
        })
    else:
        return JsonResponse({
            "error": "Invalid Request"
        })


@csrf_exempt
def update_product(request, id):
    if request.method == "GET":
        print(F"GET : {id}")
        required_product = PRODUCTS[id]
        return JsonResponse(required_product)
    
    elif request.method == "PUT":
        print(f"UPDATE : {id}")
        data = json.loads(request.body.decode("utf-8"))
        for key in data.keys():
            PRODUCTS[id][key] = data[key]
        return JsonResponse({
            "message" : f"Product Updated Successfully",
            "product id" : id
        })
    
    elif request.method == "DELETE":
        print(f"DELETE: {id}")
        del PRODUCTS[id]
        return JsonResponse({
            "message" : f"Product with id {id} deleted"
        })
    
    else: 
        return JsonResponse({
            "error": f"Invalid request"
        })