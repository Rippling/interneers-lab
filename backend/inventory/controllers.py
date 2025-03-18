from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import ProductService
import json


def get_all_products(request):
    products = ProductService.get_all_products()
    return JsonResponse({"products": products})

def get_product_by_id(request, id):
    product = ProductService.get_product_by_id(id)
    if product:
        return JsonResponse(product)
    return JsonResponse({"error" : "Product not found"}, status = 404)

@csrf_exempt
def create_product(request):
    data = json.loads(request.body.decode("utf-8"))
    response = ProductService.create_new_product(data)
    return JsonResponse(response)

@csrf_exempt
def update_product(request, id):
    data = json.loads(request.body.decode("utf-8"))
    response = ProductService.update_product(id, data)
    return JsonResponse(response)

@csrf_exempt
def delete_product(request, id):
    response = ProductService.delete_product(id)
    return JsonResponse(response) 

