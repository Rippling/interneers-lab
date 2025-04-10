"""
This module is the controller for all product related endpoints.

All requests to the /product endpoint are to be routed to productEndpoint(request, request_id). 
Rest are functions that implement specific method endpoints, or helper functions.
"""

#pylint: disable=no-member

import json
import math
from django.http import HttpRequest, JsonResponse
from src.utils.error import generate_error_response

from src.models.product import create_product, Product

from mongoengine.errors import DoesNotExist, ValidationError


def product_endpoint(request: HttpRequest, request_id: str= None):
    """
    This is the function that handles all requests to /product and /product/<id>.

    All requests are initially routed to this function, then this function calls the 
    appropriate functions for given methods. 

    Args:
        request: An HttpRequest instance created by Django
        request_id: for /product/<id> request, this is the integer id, to refer to a 
        particular product. 0 is reserved for collection requests. The default value
        is zero, that is, a GET request defaults to a collection request.
    
    Returns:
        The appropriate JsonResponse object, based on the request.
    """

    if request.method== "GET":
        return get_product(request, request_id)
    if request.method== "POST":
        return add_product(request)
    if request.method== "PATCH":
        return update_product(request, request_id)
    if request.method== "DELETE":
        return delete_product(request, request_id)
    else:
        details= f"No endpoint for {request.method} request"
        suggestion= "Check the documentation at https://github.com/Alph3ga/interneers-lab " \
            "for the available API endpoints"
        return generate_error_response(request, 405, details, suggestion)


def add_product(request: HttpRequest):
    """
    Controller to add a product to the database.

    Called when the request is POST /products.

    Args:
        request: An HttpRequest instance created by django. The request body must only contain
        the json representation of a product object.
    
    Returns:
        JsonResponse instance, with payload containing json representation of added object,
        and header field Location containing location where it was added. Successful response
        code is 201.
    """

    data= json.loads(request.body)
    validation= validate_product(data)  # Validate the product data recieved

    if not validation["valid"]:
        details= validation["details"]
        suggestion= validation["suggestion"]
        return generate_error_response(request, 400, details, suggestion)

    product= create_product(data)

    product.save()  # TODO: validation error

    response= JsonResponse(json.loads(product.to_json()), safe=False)
    response.status_code= 201
    response.headers["Location"]= f"/products/{product.id}"  # Location of resource
    return response


def get_product(request: HttpRequest, request_id: str):
    """
    Controller to fetch a product from the database.

    Called when the request is POST /products or /products/<id>. The logic for /products, i.e.,
    the collection request, is implemented in get_product_paginated.

    Args:
        request: An HttpRequest instance created by django. Query params can be used to specify
        pagination attributes for collection request.
    
    Returns:
        JsonResponse instance, with payload containing json representation of requested object.
        Successful response code is 200.
    """

    if request_id is not None: # Reserve 0 id for collection requests
        try:
            product= Product.objects.get(id= request_id)
        except (DoesNotExist, ValidationError) as _:
            details= f"Product with id {request_id} does not exist"
            suggestion= "Use 'GET /products' to get a list of existing products with id"
            return generate_error_response(request, 404, details, suggestion)
        return JsonResponse(json.loads(product.to_json()), safe= False)
    return get_product_paginated(request)


def get_product_paginated(request: HttpRequest):
    """
    Controller to fetch paginated list of products from the database.

    Called when the request is POST /products. Pagination is done with a start offset and a 
    page limit. 

    Args:
        request: An HttpRequest instance created by django. Query params can be used to specify
        pagination attributes for collection request. 'start' denotes the offset of the page,
        which must be a valid product id. 'limit' denotes the maximum number of products in a 
        page. 'limit' cannot be more than 250.
    
    Returns:
        JsonResponse instance, with payload containing json representation of requested object.
        Successful response code is 200. Payload also contains navigation details in the form
        {
            self: URI of current page
            next: URI of next page
            prev: URI of previous page
            pages: Total number of pages
            current: Current page number (calculated as ceil((index of first product+1)/limit))
        }
    """

    try:
        start_id= int(request.GET.get("start", "0"))
    except ValueError:
        details= f"start parameter {request.GET.get("start", "0")} could not be " \
            "converted to integer"
        suggestion= "Check if start parameter is an integer, or omit the start parameter " \
            "and use response navigation URIs to navigate"
        return generate_error_response(request, 400, details, suggestion)

    try:
        limit= int(request.GET.get("limit", "100"))
    except ValueError:
        details= f"limit parameter {request.GET.get("limit", "100")} could not be " \
            "converted to integer"
        suggestion= "Check if limit parameter is an integer, or omit the limit parameter " \
            "to use default 100 limit"
        return generate_error_response(request, 400, details, suggestion)

    if limit>250:  # Upper limit on the number of items per page
        details= f"limit parameter {request.GET.get("limit", "100")} is larger " \
            "than the maximum allowed value (250)"
        suggestion= "Resubmit request with smaller limit"
        return generate_error_response(request, 400, details, suggestion)

    # Find the index in the list to start from (if the ID exists)
    start_index= start_id

    num_products= Product.objects.count()

    # Range ends at end_index-1
    end_index= start_index+ limit if start_index+limit<num_products else num_products
    pages= math.ceil(num_products/limit)

    # prev link always points to a valid URI, unlike next, which can be null
    # in case there are less than limit products before the current start,
    # prev link always points to the page starting from the first product
    # i.e., the product with the lowest existing id
    prev_index= start_index- limit if start_index>=limit else 0

    response= JsonResponse({
        "data":json.loads(Product.objects[start_index:end_index].to_json()),
        "navigation":{
            "self": f"{request.path}/?start={start_id}&limit={limit}",
            "next": f"{request.path}/?start={end_index}&limit={limit}" \
                if end_index<num_products else None,
            "prev": f"{request.path}/?start={prev_index}&limit={limit}" \
                if prev_index>-1 else None,
            "pages": pages,
            "current": math.ceil((start_index+1)/limit)
        }
    }, safe= False)
    response.status_code= 206  # Partial content
    return response


def update_product(request: HttpRequest, request_id: int):
    """
    Controller to (partially) update a product in the database.

    Called when the request is PATCH /products/<id>. Only the id field cannot be modified.

    Args:
        request: An HttpRequest instance created by django. Payload must only contain the
        fields to be modified.
    
    Returns:
        JsonResponse instance, with no content. Successful response code is 204.
    """

    data= json.loads(request.body)

    try:
        request_product= Product.objects.get(id=request_id)
    except DoesNotExist:
        details= f"Product with id {request_id} does not exist"
        suggestion= "Use 'GET /products' to get a list of existing products with id"
        return generate_error_response(request, 404, details, suggestion)

    # Modify each key specified in the request
    for key in data.keys():
        if key=="id":
            details: "Product ID cannot be updated"
            suggestion: "Remove 'id' field from your request, or check if it matches the URI"
            return generate_error_response(request, 400, details, suggestion)
    request_product.modify_fields(data)

    response= JsonResponse({})
    response.headers["Location"]= f"/products/{request_product.id}"  # Location of resource
    response.status_code= 204  # No content in body
    return response


def delete_product(request: HttpRequest, request_id: str):
    """
    Controller to delete a product in the database.

    Called when the request is DELETE /products/<id>. ID must be valid.

    Args:
        request: An HttpRequest instance created by django. Payload does not matter.
    
    Returns:
        JsonResponse instance, with no content. Successful response code is 204.
    """

    try:
        Product.objects.get(id=request_id).delete()
    except DoesNotExist:
        details= f"Product with id {request_id} does not exist"
        suggestion= "Use 'GET /products' to get a list of existing products with id"
        return generate_error_response(request, 404, details, suggestion)

    response= JsonResponse({})
    response.status_code= 204
    return response


def validate_product(data: dict) -> dict:
    """
    Validates product data recieved in request.

    Checks necessary fields, name, price, and quantity. Does not yet validate the integrity of
    optional fields, or ensure only the specified fields exist.

    Args:
        data: dict instance, obtained from the json representation of product given in a request.

    Returns:
        dict instance, with "valid" (boolean) indicating validation status. If they exist, 
        "details" indicates error details, and "suggestion" indicates suggestions to fix
        the error.
    """

    if "name" not in data:
        return {
            "valid": False,
            "details": "'name' field is required for the product",
            "suggestion": "Re-send the request with an appropriate name field",
        }
    if not isinstance(data["name"], str) or len(data["name"])== 0:
        return {
            "valid": False,
            "details": "'name' field is invalid",
            "suggestion": "Re-send the request with an appropriate name field, it must be " \
            "a non-empty string",
        }


    if "price" not in data:
        return {
            "valid": False,
            "details": "'price' field is required for the product",
            "suggestion": "Re-send the request with an appropriate price field " \
            "(non-negative integer)",
        }
    if not isinstance(data["price"], int) or data["price"]< 0:
        return {
            "valid": False,
            "details": "'price' field is invalid",
            "suggestion": "Re-send the request with an appropriate price field, it must be a " \
            "non-negative integer. Check if you are sending a string instead",
        }

    if "quantity" not in data:
        return {
            "valid": False,
            "details": "'quantity' field is required for the product",
            "suggestion": "Re-send the request with an appropriate quantity field " \
            "(non-negative integer)",
        }
    if not isinstance(data["quantity"], int) or data["quantity"]< 0:
        return {
            "valid": False,
            "details": "'quantity' field is invalid",
            "suggestion": "Re-send the request with an appropriate quantity field, it must " \
            "be a non-negative integer. Check if you are sending a string instead",
        }

    return { "valid": True}

