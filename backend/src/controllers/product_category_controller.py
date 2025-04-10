"""
This module is the controller for all category-product related endpoints.

All requests to the /category/<title> endpoint are to be routed to 
category_product_endpoint(request, category_title).
Rest are functions that implement specific method endpoints, or helper functions.
"""

#pylint: disable=no-member

import json
from django.http import HttpRequest, JsonResponse
from src.utils.error import generate_error_response
from src.services.product_category_service import ProductCategoryService
from mongoengine.errors import DoesNotExist, ValidationError


def category_product_endpoint(request: HttpRequest, category_title: str):
    """
    This is the function that handles all requests to /category/<title>.

    Args:
        request: An HttpRequest instance created by Django
        category_title: The slug (title) of the category

    Returns:
        JsonResponse based on the type of HTTP request
    """

    if request.method == "GET":
        return get_products_in_category(request, category_title)
    if request.method == "POST":
        return add_product_to_category(request, category_title)
    if request.method == "DELETE":
        return remove_product_from_category(request, category_title)
    else:
        details = f"No endpoint for {request.method} request"
        suggestion = "Use GET, POST, or DELETE on /category/<title>"
        return generate_error_response(request, 405, details, suggestion)


def get_products_in_category(request: HttpRequest, category_title: str):
    """
    Controller to list products under a specific category.

    Args:
        request: HttpRequest object
        category_title: Title of the category

    Returns:
        JsonResponse with list of products
    """
    try:
        category = ProductCategoryService.get_category_by_title(category_title)
        products = ProductCategoryService.list_products_in_category(category.id)
        return JsonResponse(json.loads(products.to_json()), safe=False)
    except DoesNotExist:
        details = f"Category with title '{category_title}' does not exist"
        suggestion = "Use a valid category title"
        return generate_error_response(request, 404, details, suggestion)


def add_product_to_category(request: HttpRequest, category_title: str):
    """
    Controller to add a product to a category.

    Args:
        request: HttpRequest object
        category_title: Title of the category

    Returns:
        JsonResponse with the updated product
    """
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        if not product_id:
            return generate_error_response(
                request, 400, "Missing 'product_id'", "Include 'product_id' in the request body"
            )

        # Optional: Validate product structure (example)
        validation = validate_product(data)
        if not validation["valid"]:
            return generate_error_response(request, 400, validation["details"], validation["suggestion"])

        category = ProductCategoryService.get_category_by_title(category_title)
        product = ProductCategoryService.add_product_to_category(product_id, category.id)
        return JsonResponse(json.loads(product.to_json()), safe=False, status=200)
    except DoesNotExist:
        return generate_error_response(request, 404, "Category or Product not found", "Check category title and product ID")
    except ValidationError:
        return generate_error_response(request, 400, "Invalid data provided", "Check the format of the product ID")


def remove_product_from_category(request: HttpRequest, category_title: str):
    """
    Controller to remove a product from a category.

    Args:
        request: HttpRequest object
        category_title: Title of the category (not used directly)

    Returns:
        JsonResponse with the updated product
    """
    try:
        data = json.loads(request.body)
        product_id = data.get("product_id")
        if not product_id:
            return generate_error_response(
                request, 400, "Missing 'product_id'", "Include 'product_id' in the request body"
            )

        product = ProductCategoryService.remove_product_from_category(product_id)
        return JsonResponse(json.loads(product.to_json()), safe=False, status=200)
    except DoesNotExist:
        return generate_error_response(request, 404, "Product not found", "Check product ID")
    except ValidationError:
        return generate_error_response(request, 400, "Invalid product ID", "Check the format of the product ID")


def validate_product(data: dict) -> dict:
    """
    Validates product data received in request.

    Args:
        data: dict representing product data

    Returns:
        dict with "valid", "details", and "suggestion" fields
    """
    if "name" not in data or not isinstance(data["name"], str) or len(data["name"]) == 0:
        return {
            "valid": False,
            "details": "'name' field is required and must be a non-empty string",
            "suggestion": "Provide a valid 'name' field"
        }

    if "price" not in data or not isinstance(data["price"], int) or data["price"] < 0:
        return {
            "valid": False,
            "details": "'price' field is required and must be a non-negative integer",
            "suggestion": "Provide a valid 'price' field"
        }

    if "quantity" not in data or not isinstance(data["quantity"], int) or data["quantity"] < 0:
        return {
            "valid": False,
            "details": "'quantity' field is required and must be a non-negative integer",
            "suggestion": "Provide a valid 'quantity' field"
        }

    if "description" in data and (not isinstance(data["description"], str) or len(data["description"]) > 250):
        return {
            "valid": False,
            "details": "'description' must be a string with max length 250 characters",
            "suggestion": "Shorten or format 'description' field appropriately"
        }

    return {"valid": True}
