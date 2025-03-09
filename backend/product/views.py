from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

# List of products
PRODUCTS = []
PRODUCT_ID = 1


@csrf_exempt
def create_product(request):
    """
    Handles product creation with data validation.
    """
    global PRODUCT_ID  

    if request.method != "POST":
        return JsonResponse({"error": "Use POST method to create a product."}, status=405)

    try:
        data = json.loads(request.body)

        required_fields = ["name", "description", "category", "price_in_RS", "brand", "quantity", "manufacture_date", "expiry_date", "weight_in_KG"]
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"{field} is required."}, status=400)

        # Validate data types
        if not isinstance(data["price_in_RS"], (int, float)) or data["price_in_RS"] <= 0:
            return JsonResponse({"error": "Price must be a positive number."}, status=400)
        if not isinstance(data["quantity"], int) or data["quantity"] < 0:
            return JsonResponse({"error": "Quantity must be a non-negative integer."}, status=400)

        try:
            manufacture_date = datetime.strptime(data["manufacture_date"], "%Y-%m-%d")
            expiry_date = datetime.strptime(data["expiry_date"], "%Y-%m-%d")
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        if expiry_date <= manufacture_date:
            return JsonResponse({"error": "Expiry date must be after manufacture date."}, status=400)

        # Create product
        product = {
            "id": PRODUCT_ID,
            "name": data["name"],
            "description": data["description"],
            "category": data["category"],
            "price_in_RS": data["price_in_RS"],
            "brand": data["brand"],
            "quantity": data["quantity"],
            "manufacture_date": data["manufacture_date"],
            "expiry_date": data["expiry_date"],
            "weight_in_KG": data["weight_in_KG"]
        }

        PRODUCTS.append(product)  
        PRODUCT_ID += 1  

        return JsonResponse({"message": "Product created successfully!", "id": product["id"]}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt       
def get_product(request, product_id):
    """
    Fetches a product by ID.
    """
    if request.method != "GET":
        return JsonResponse({"error": "Use GET method to fetch a product."}, status=405)

    if not isinstance(product_id, int):
        return JsonResponse({"error": "Invalid product ID."}, status=400)

    for product in PRODUCTS:
        if product["id"] == product_id:
            return JsonResponse(product, status=200)

    return JsonResponse({"error": "Product not found"}, status=404)


@csrf_exempt
def get_all_products(request):
    """
    Fetches all products.
    """
    if request.method != "GET":
        return JsonResponse({"error": "Use GET method to fetch all products."}, status=405)

    return JsonResponse({"Available Products": PRODUCTS}, status=200)


@csrf_exempt
def update_product(request, product_id):
    """
    Updates an existing product with validation.
    """
    if request.method != "PUT":
        return JsonResponse({"error": "Use PUT method to update a product."}, status=405)

    try:
        data = json.loads(request.body)

        for product in PRODUCTS:
            if product["id"] == product_id:
                # Validate price and quantity if provided
                if "price_in_RS" in data and (not isinstance(data["price_in_RS"], (int, float)) or data["price_in_RS"] <= 0):
                    return JsonResponse({"error": "Price must be a positive number."}, status=400)
                if "quantity" in data and (not isinstance(data["quantity"], int) or data["quantity"] < 0):
                    return JsonResponse({"error": "Quantity must be a non-negative integer."}, status=400)

                # Validate and update dates if provided
                if "manufacture_date" in data or "expiry_date" in data:
                    try:
                        manufacture_date = datetime.strptime(data.get("manufacture_date", product["manufacture_date"]), "%Y-%m-%d")
                        expiry_date = datetime.strptime(data.get("expiry_date", product["expiry_date"]), "%Y-%m-%d")
                        if expiry_date <= manufacture_date:
                            return JsonResponse({"error": "Expiry date must be after manufacture date."}, status=400)
                    except ValueError:
                        return JsonResponse({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

                product.update(data)
                return JsonResponse({"message": "Product details updated successfully!"}, status=200)

        return JsonResponse({"error": "Product not found"}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format."}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def delete_product(request, product_id):
    """
    Deletes a product by ID.
    """
    if request.method != "DELETE":
        return JsonResponse({"error": "Use DELETE method to delete a product."}, status=405)

    if not isinstance(product_id, int):
        return JsonResponse({"error": "Invalid product ID."}, status=400)

    for index, product in enumerate(PRODUCTS):
        if product["id"] == product_id:
            del PRODUCTS[index]  
            return JsonResponse({"message": "Product deleted successfully"}, status=200)

    return JsonResponse({"error": "Product not found: incorrect ID"}, status=404)
