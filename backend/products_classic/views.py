from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product

# Utility to serialize Product
def serialize_product(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": str(product.price),
        "brand": product.brand,
        "quantity_in_warehouse": product.quantity_in_warehouse
    }


# Validation Utility
def validate_product_data(data):
    errors = []
    required_fields = ['name', 'description', 'category', 'price', 'brand', 'quantity_in_warehouse']

    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field} is required.")
    
    if 'price' in data and (not isinstance(data['price'], (int, float)) or data['price'] < 0):
        errors.append("Price must be a non-negative number.")

    if 'quantity_in_warehouse' in data and (not isinstance(data['quantity_in_warehouse'], int) or data['quantity_in_warehouse'] < 0):
        errors.append("Quantity must be a non-negative integer.")
    
    return errors


# Create a new product
# Added validation and error check
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            errors = validate_product_data(data)
            if errors:
                return JsonResponse({"errors": errors}, status=400)
            product = Product.objects.create(**data)
            return JsonResponse(serialize_product(product), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "POST method required"}, status=405)

# Fetch all products
# Added Pagination
def get_products(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page',1))
            page_size = int(request.GET.get('page_size',5))
            start = (page - 1) * page_size
            end = start + page_size
            
            products = Product.objects.all()
            data = [serialize_product(p) for p in products[start:end]]
            total_products = products.count()
            
            return JsonResponse({
                "total": total_products,
                "page": page,
                "page_size": page_size,
                "products": data
            }, safe=False)
        except ValueError:
            return JsonResponse({"error": "Invalid pagination parameters."}, status=400)
    return JsonResponse({"error": "GET method required"}, status=405)

# Fetch a single product
#Better detailed error message
def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        return JsonResponse(serialize_product(product))
    except Product.DoesNotExist:
        return JsonResponse({"error": f"Product with ID {pk} not found."}, status=404)

# Update a product
# Added Validation check and error Check
@csrf_exempt
def update_product(request, pk):
    if request.method == 'PUT':
        try:
            product = Product.objects.get(pk=pk)
            data = json.loads(request.body)
            errors = validate_product_data(data)
            if errors:
                return JsonResponse({"errors":errors}, status=400)
            
            for field in ['name', 'description', 'category', 'price', 'brand', 'quantity_in_warehouse']:
                if field in data:
                    setattr(product, field, data[field])
            product.save()
            return JsonResponse(serialize_product(product))
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "PUT method required"}, status=405)

# Delete a product
@csrf_exempt
def delete_product(request, pk):
    if request.method == 'DELETE':
        try:
            product = Product.objects.get(pk=pk)
            product.delete()
            return JsonResponse({"message": f"Product with ID {pk} has been deleted."}, status=204)
        except Product.DoesNotExist:
            return JsonResponse({"error": f"Product with ID {pk} not found."}, status=404)
    return JsonResponse({"error": "DELETE method required"}, status=405)
