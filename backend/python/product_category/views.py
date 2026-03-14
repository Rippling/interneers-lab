import json
from .services import ProductCategoryService
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def create_product_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_category = ProductCategoryService.create_product_category(data)
        return JsonResponse({
            "id": str(product_category.id),
            "name": product_category.name,
            "description": product_category.description,
            "message": "Product category created"
        })
    return {"error": "Invalid request method"}

def get_all_product_categories(request):
    if request.method == 'GET':
        product_categories = ProductCategoryService.get_all_product_categories()
        return JsonResponse({
            "product_category": [
                {
                    "id": str(pc.id),
                    "name": pc.name,
                    "description": pc.description
                }
                for pc in product_categories
            ]
        })
    return {"error": "Invalid request method"}

def get_product_category_by_id(request, product_category_id):
    if request.method == 'GET':
        try:
            product_category = ProductCategoryService.get_product_category_by_id(product_category_id)
            return JsonResponse({
                "id": str(product_category.id),
                "name": product_category.name,
                "description": product_category.description
            })
        except ValueError as e:
            return {"error": str(e)}
    return {"error": "Invalid request method"}

@csrf_exempt
def update_product_category(request, product_category_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            product_category = ProductCategoryService.update_product_category(product_category_id, data)
            return JsonResponse({
                "id": str(product_category.id),
                "name": product_category.name,
                "description": product_category.description
            })
        except ValueError as e:
            return {"error": str(e)}
    return {"error": "Invalid request method"}

@csrf_exempt
def delete_product_category(request, product_category_id):
    if request.method == 'DELETE':
        product_category = ProductCategoryService.delete_product_category(product_category_id)
        if product_category:
            return JsonResponse({"message": "Product category deleted"})
        else:
            return JsonResponse({"error": "Product category not found"})
    return {"error": "Invalid request method"}
    