import json

from rest_framework.decorators import api_view
from django.http import JsonResponse
from ..services.product_service import ProductService
from ..services.category_service import CategoryService
from ..serializers import *
from ..exceptions import *
from ..validators import *
from ..responses import *

product_service = ProductService()
category_service = CategoryService()

@api_view(["GET", "POST"])
def categories(request):

    if request.method == "GET":
        categories = category_service.get_all_categories()
        serialized_categories = [serialize_catgeory(category) for category in categories] 
        return success_response("categories",serialized_categories, 200)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body) 
            data=validate_category(data)
            category = category_service.create_category(data)
            serialized_category = serialize_catgeory(category)
            return success_response("category created",serialized_category, 201)
        except InvalidData as e:  
            return error_response(str(e), 400)

    else:
        return invalid_method_response()
@api_view(["GET","PUT","PATCH","DELETE"])    
def category_detail(request, category_id):
   
    if request.method == "GET":
        try:
            category = category_service.get_category(category_id)
            serialized_category = serialize_catgeory(category)
            return success_response("category",serialized_category, 200)
        except CategoryError as e:
            return error_response(e.message, e.status_code)
        
    elif request.method == "PUT":    
        try:    
            data = json.loads(request.body)
            data=validate_category(data)
            category = category_service.update_category(category_id, data)
            serialized_category = serialize_catgeory(category)
            return success_response("category updated",serialized_category, 200)
        except CategoryError as e:
            return error_response(e.message, e.status_code)
        except InvalidData as e:
            return error_response(str(e), 400)
        
    elif request.method == "PATCH":
        try:
            data = json.loads(request.body)
            data=validate_category(data,[])
            category = category_service.update_category(category_id, data, fields_required=False)
            serialized_category = serialize_catgeory(category)
            return success_response("category updated",serialized_category, 200)
        except CategoryError as e:
            return error_response(e.message, e.status_code)
        except InvalidData as e:
            return error_response(str(e), 400)
        
    elif request.method == "DELETE":
        try:
            category=category_service.delete_category(category_id)
            return success_response("category deleted",serialize_catgeory(category), 200)
        except CategoryError as e:
            return error_response(e.message, e.status_code)      
    else:
        return invalid_method_response()


@api_view(["GET"])
def list_products_by_category_id(request, category_id):
    if request.method == "GET":
        try:
            sort_by=request.GET.get("sort_by","-updated_at")    
            category_service.get_category(category_id) 
        except CategoryError as e:
            return error_response(e.message, e.status_code)
        
        products = product_service.list_products_by_category_id(category_id, sort_by)
        serialized_products = [serialize_product(product) for product in products]
        return success_response("products",serialized_products, 200)
    else:
        return invalid_method_response()