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

    return JsonResponse([
            {
                "id": str(p.id),
                "name": p.name,
                "description": p.description,
                "price": p.price
            }
            for p in products
        ], safe=False)


def get_product(request, product_id):
    try:
        product=ProductServices.get_product(product_id)
        return JsonResponse({
            "id" : str(product.id),
            "name": product.name,
            "description" : product.description,
            "price" : product.price,
        })
    except ValueError as er:
        return JsonResponse({"error" : str(er)}, status=404)

@csrf_exempt
def delete_product(request, product_id):
    if request.method == "DELETE":
        ProductServices.delete_product(product_id)
        return JsonResponse({"message":"Deleted"})
    else:
        return JsonResponse({"error" : "DELETE method not used"}, status=400)