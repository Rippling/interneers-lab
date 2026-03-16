import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import ProductServices

@csrf_exempt
def create_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            product = ProductServices.create_product(data)
            return JsonResponse({
                "id": str(product.id),
                "message": "Product created"
            })
        except ValueError as er:
            return JsonResponse({"error": str(er)}, status=400)
        
    return JsonResponse({"error" : "POST method not used"}, status=400)
        

def list_products(request):
    products = ProductServices.list_products()

    response_data = []
    for p in products:
       
        raw_category = p._data.get('category')
        
        cat_id = str(raw_category.id) if raw_category else None

        response_data.append({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "category": cat_id
        })

    return JsonResponse(response_data, safe=False)


def get_product(request, product_id):
    try:
        product=ProductServices.get_product(product_id)
        raw_category = product._data.get('category')
       
        cat_id = str(raw_category.id) if raw_category else None
        return JsonResponse({
            "id" : str(product.id),
            "name": product.name,
            "description" : product.description,
            "price" : product.price,
            "category": cat_id
        })
    except ValueError as er:
        return JsonResponse({"error" : str(er)}, status=404)

@csrf_exempt
def list_products_by_category_id(request, category_id):
    if request.method == "GET":
        products = ProductServices.list_products_by_category_id(category_id)

        return JsonResponse([
            {
                "id": str(p.id),
                "name": p.name,
                "description": p.description,
                "price": p.price
            }
            for p in products
        ], safe=False)
    else:
        return JsonResponse({"error" : "GET method not used"}, status=400)

@csrf_exempt
def remove_category_from_product(request, product_id):
    if request.method == "PATCH":
        try:
            product = ProductServices.remove_category_from_product(product_id)
            return JsonResponse({
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": None
            },status=200)
        except ValueError as er:
            return JsonResponse({"error": str(er)}, status=404)
    else:
        return JsonResponse({"error" : "PATCH method not used"}, status=400)
    
@csrf_exempt
def add_category_to_product(request, product_id, category_id):
    if request.method == "PATCH":
        try:
            product = ProductServices.add_category_to_product(product_id, category_id)
            return JsonResponse({
                "id": str(product.id),
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": str(product.category.id) if product.category else None
            })
        except ValueError as er:
            return JsonResponse({"error": str(er)}, status=404)
    else:
        return JsonResponse({"error" : "PATCH method not used"}, status=400)    

@csrf_exempt
def delete_product(request, product_id):
    if request.method == "DELETE":
        ProductServices.delete_product(product_id)
        return JsonResponse({"message":"Deleted"})
    else:
        return JsonResponse({"error" : "DELETE method not used"}, status=400)