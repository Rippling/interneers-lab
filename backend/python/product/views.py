import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .data import products


@csrf_exempt
def create_product(request):
    # GET → fetch all products
    if request.method == "GET":
        return JsonResponse({"products": products})

    # POST → create product
    if request.method == "POST":
        data = json.loads(request.body)

        required_fields = ["name", "price", "category", "brand", "quantity"]
        for field in required_fields:
            if field not in data:
                return JsonResponse(
                    {"error": f"{field} is required"},
                    status=400
                )

        if data["price"] <= 0:
            return JsonResponse(
                {"error": "Price must be positive"},
                status=400
            )

        product = Product(
            id=len(products) + 1,
            name=data["name"],
            description=data.get("description", ""),
            category=data["category"],
            price=data["price"],
            brand=data["brand"],
            quantity=data["quantity"]
        )

        products.append(product.__dict__)

        return JsonResponse(
            {"message": "Product created", "product": product.__dict__},
            status=201
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_product(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    for product in products:
        if product["id"] == id:
            return JsonResponse(product)

    return JsonResponse({"error": "Product not found"}, status=404)


@csrf_exempt
def update_product(request, id):
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)

    for product in products:
        if product["id"] == id:
            product.update(data)
            return JsonResponse(
                {"message": "Product Updated", "product": product}
            )

    return JsonResponse({"error": "Product not found"}, status=404)


@csrf_exempt
def delete_product(request, id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    global products
    products = [p for p in products if p["id"] != id]
    return JsonResponse({"message": "Product deleted"})
