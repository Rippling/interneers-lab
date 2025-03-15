from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = Product(**data)
            product.save()
            return JsonResponse({"message": "Product created", "id": str(product.id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def get_product(request, product_id):
    try:
        # Validate and convert product_id to ObjectId
        if not ObjectId.is_valid(product_id):
            return JsonResponse({"error": "Invalid ObjectId"}, status=400)

        product = Product.objects.get(id=ObjectId(product_id))

        return JsonResponse({
            "id": str(product.id),
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "price": str(product.price),  # Ensure JSON serialization works
            "brand": product.brand,
            "quantity": product.quantity,
        })
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

def list_products(request):
    try:
        products = Product.objects()
        
        # Convert each product to a dictionary and ensure ObjectId is converted to a string
        product_list = []
        for product in products:
            product_dict = product.to_mongo().to_dict()
            product_dict["_id"] = str(product_dict["_id"])  # Convert ObjectId to string
            product_list.append(product_dict)

        return JsonResponse(product_list, safe=False)

    except Exception as e:
        return JsonResponse({"error": f"Internal Server Error: {str(e)}"}, status=500)

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            # Validate ObjectId
            if not ObjectId.is_valid(product_id):
                return JsonResponse({"error": "Invalid ObjectId"}, status=400)

            data = json.loads(request.body)
            updated_count = Product.objects.filter(id=ObjectId(product_id)).update(**data)

            if updated_count == 0:
                return JsonResponse({"error": "Product not found"}, status=404)

            return JsonResponse({"message": "Product updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        try:
            # Validate ObjectId
            if not ObjectId.is_valid(product_id):
                return JsonResponse({"error": "Invalid ObjectId"}, status=400)

            deleted = Product.objects(id=ObjectId(product_id)).delete()

            if deleted == 0:
                return JsonResponse({"error": "Product not found"}, status=404)

            return JsonResponse({"message": "Product deleted successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
