import json

from rest_framework.decorators import api_view
from ..services.product_service import ProductService
from ..services.category_service import CategoryService
from ..serializers import *
from ..exceptions import *
from ..validators import *
from ..responses import *

product_service = ProductService()
category_service = CategoryService()
@api_view(["GET", "POST"])
def products(request):

    if request.method == "GET":
        sort_by=request.GET.get("sort_by","-updated_at")
        products = product_service.list_products(sort_by)
        serialized_products = [serialize_product(product) for product in products]
        return success_response("products",serialized_products, 200)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            data=validate_product(data)
            product = product_service.create_product(data)
            serialized_product = serialize_product(product)
            return success_response("product created",serialized_product, 201)
        except InvalidData as e:
            return error_response(str(e), 400)
    else:
        return invalid_method_response()
    
@api_view(["GET","PUT","PATCH","DELETE"])
def product_detail(request, product_id):
   
    if request.method == "GET":
        try:
            product = product_service.get_product(product_id)
            serialized_product = serialize_product(product)
            return success_response("product",serialized_product, 200)
        except ProductError as e:
           return error_response(e.message, e.status_code)
        

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            data=validate_product(data)
            product = product_service.update_product(product_id, data)
            serialized_product = serialize_product(product)
            return success_response("product updated",serialized_product, 200)  
        except (ProductError,CategoryError) as e:
            return error_response(e.message,e.status_code)
        except InvalidData as e:
            return error_response(str(e), 400)
        
    elif request.method == "PATCH":
        try:
            data = json.loads(request.body)
            data=validate_product(data, [])
            product = product_service.update_product(product_id, data)
            serialized_product = serialize_product(product)
            return success_response("product updated",serialized_product, 200)
        except ProductError as e:
            return error_response(e.message, e.status_code)
        except InvalidData as e:
           return error_response(str(e), 400)

    elif request.method == "DELETE":

        try:
            product = product_service.delete_product(product_id)
            return success_response("product deleted",serialize_product(product), 200)
        except ProductError as e:
            return error_response(e.message, e.status_code)
        
    else:
        return invalid_method_response()
    