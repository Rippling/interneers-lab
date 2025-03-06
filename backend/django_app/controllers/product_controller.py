"""
This module is the controller for all product related endpoints.

All requests to the /product endpoint are to be routed to productEndpoint(request, request_id). 
Rest are functions that implement specific method endpoints, or helper functions.
"""

import json
from datetime import datetime
import math
from django.http import HttpRequest, JsonResponse

products= []


def product_endpoint(request: HttpRequest, request_id: int= 0):
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
        error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": f"No endpoint for {request.method} request",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Check the documentation at https://github.com/Alph3ga/interneers-lab " \
                "for the available API endpoints"
            })
        error_response.status_code= 400
        return error_response


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
        error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": validation["details"],
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": validation["suggestion"],
            })
        error_response.status_code= 400  # TODO: Change this to a 405 Method not found error
        return error_response

    data["id"]= len(products)+1
    products.append(data)

    response= JsonResponse(data)
    response.status_code= 201
    response.headers["Location"]= f"/products/{data["id"]}"  # Location of resource
    return response


def get_product(request: HttpRequest, request_id: int):
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

    if request_id!=0: # Reserve 0 id for collection requests
        index= find_product(request_id)

        if index== -1:
            error_response= JsonResponse({
                "code": "NOT_FOUND",
                "message": "The requested resource was not found",
                "details": f"Product with id {request_id} does not exist",
                "timestamp": f"{datetime.now()} GMT+0:00",
                "request": f"{request.method} {request.path}",
                "suggestion": "Use 'GET /products' to get a list of existing products with id",
                })
            error_response.status_code= 404
            return error_response
        return JsonResponse(products[index])
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
        error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The requested resource was not found",
            "details": f"start parameter {request.GET.get("start", "0")} could not be " \
                "converted to integer",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Check if start parameter is an integer, or omit the start parameter " \
                "and use response navigation URIs to navigate",
            })
        error_response.status_code= 400
        return error_response

    try:
        limit= int(request.GET.get("limit", "100"))
    except ValueError:
        error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": f"limit parameter {request.GET.get("limit", "100")} could not be " \
                "converted to integer",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Check if limit parameter is an integer, or omit the limit parameter " \
                "to use default 100 limit",
            })
        error_response.status_code= 400
        return error_response

    if limit>250:
        error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": f"limit parameter {request.GET.get("limit", "100")} is larger " \
                "than the maximum allowed value (250)",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Resubmit request with smaller limit",
            })
        error_response.status_code= 400
        return error_response

    # Find the index in the list to start from (if the ID exists)
    start_index= find_product(start_id) if start_id>0 else 0
    if start_index==-1:
        error_response= JsonResponse({
            "code": "NOT_FOUND",
            "message": "The server cannot process this request",
            "details": f"start parameter {request.GET.get("start", "0")} is not a ID " \
                "that exists in the database",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Check if the you have deleted the product, or omit the start " \
                "parameter and use response navigation URIs to navigate",
            })
        error_response.status_code= 404
        return error_response

    # Range ends at end_index-1
    end_index= start_index+ limit if start_index+limit<len(products) else len(products)+1
    pages= math.ceil(len(products)/limit)

    # prev link always points to a valid URI, unlike next, which can be null
    # in case there are less than limit products before the current start,
    # prev link always points to the page starting from the first product
    # i.e., the product with the lowest existing id
    prev_index= start_index- limit if start_index>=limit else 0

    response= JsonResponse({
        "data":products[start_index:end_index],
        "navigation":{
            "self": f"{request.path}/?start={start_id}&limit={limit}",
            "next": f"{request.path}/?start={products[end_index]["id"]}&limit={limit}" \
                if end_index<len(products) else None,
            "prev": f"{request.path}/?start={products[prev_index]["id"]}&limit={limit}" \
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

    index= find_product(request_id)
    if index== -1:
        error_response= JsonResponse({
            "code": "NOT_FOUND",
            "message": "The requested resource was not found",
            "details": f"Product with id {request_id} does not exist",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Use 'GET /products' to get a list of existing products with id",
            })
        error_response.status_code= 404
        return error_response

    request_product= products[index]

    # Modify each key specified in the request
    for key in data.keys():
        if key=="id":
            error_response= JsonResponse({
            "code": "BAD_REQUEST",
            "message": "The server cannot process this request",
            "details": "Product ID cannot be updated",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Remove 'id' field from your request, or check if it matches the URI",
            })
            error_response.status_code= 404
            return error_response
        request_product[key]= data[key]

    response= JsonResponse({})
    response.headers["Location"]= f"/products/{request_id}"  # Location of resource
    response.status_code= 204  # No content in body
    return response


def delete_product(request: HttpRequest, request_id: int):
    """
    Controller to delete a product in the database.

    Called when the request is DELETE /products/<id>. ID must be valid.

    Args:
        request: An HttpRequest instance created by django. Payload does not matter.
    
    Returns:
        JsonResponse instance, with no content. Successful response code is 204.
    """

    index= find_product(request_id)
    if index== -1:
        error_response= JsonResponse({
            "code": "NOT_FOUND",
            "message": "The requested resource was not found",
            "details": f"Product with id {request_id} does not exist",
            "timestamp": f"{datetime.now()} GMT+0:00",
            "request": f"{request.method} {request.path}",
            "suggestion": "Use 'GET /products' to get a list of existing products with id",
            })
        error_response.status_code= 404
        return error_response
    products.pop(index)

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


def find_product(request_id: int):
    """
    Finds the product index in the array based on the product id

    Args:
        request_id: the integer id of the product to find

    Returns:
        the integer index of the product, if found. -1 if not found
    """

    # binary search through the products array

    l= 0
    r= len(products)

    while l<r:
        mid= (l+r)//2
        if products[mid]["id"]== request_id:
            return mid
        if products[mid]["id"]< request_id:
            l= mid+1
        else:
            r= mid
    return -1
