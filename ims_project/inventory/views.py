import json
from turtle import pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .services import ProductService, ProductCategoryService
from .serializers import ProductSerializer, ProductCategorySerializer


product_service = ProductService()
category_service = ProductCategoryService()

def handle_value_error(e, status_code=400):
        error_detail = e.args[0] if e.args else "An error occurred"
        if isinstance(error_detail, str):
            return JsonResponse({"error": error_detail}, status=status_code)
        return JsonResponse(error_detail, status=status_code)


class ProductView:  

    @csrf_exempt
    def product_collection_view(self,request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                product = product_service.create_new_product(data)
                return JsonResponse({"id": str(product.id)}, status=201)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            except ValueError as e:
                return handle_value_error(e)

        elif request.method == 'GET':
            prod_category = request.GET.get('category','all')
            if prod_category == 'all':
                products = product_service.get_all_products()
                serializer = ProductSerializer(products, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            else :
                try:
                    products = category_service.get_products_by_category(prod_category)
                    serializer = ProductSerializer(products, many=True)
                    return JsonResponse(serializer.data, safe=False, status=200)
                except ValueError as e:
                    return handle_value_error(e)
                
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)

    @csrf_exempt
    def product_detail_view(self,request, product_id):
        if request.method == "PATCH":
            try:
                data = json.loads(request.body)
                product = product_service.update_existing_product(product_id, data)
                serializer = ProductSerializer(product)
                return JsonResponse(serializer.data, status=200)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            except ValueError as e:
                return handle_value_error(e)

        elif request.method == "DELETE":
            try:
                product_service.delete_product_record(product_id)
                return JsonResponse({"message": "Product deleted successfully."}, status=204)
            except ValueError as e:
                return handle_value_error(e)
            
        else:
            return JsonResponse({"error": "Method not allowed"}, status=405)
        
    @csrf_exempt
    def bulk_upload_view(self, request):

        if request.method != 'POST':
            return JsonResponse({"error": "Method not allowed"}, status=405)

        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file uploaded. Please upload a CSV file with the key 'file'."}, status=400)

        csv_file = request.FILES['file']
        

        if not csv_file.name.endswith('.csv'):
            return JsonResponse({"error": "File is not a CSV"}, status=400)

        try:
            df = pd.read_csv(csv_file)
            df = df.where(pd.notnull(df), None)
            product_list = df.to_dict('records')
            
            results = {
                "success_count": 0,
                "errors": []
            }
            for row_index, row_data in enumerate(product_list):
                try:
                    product_service.create_new_product(row_data)
                    results["success_count"] += 1
                except ValueError as e:
                    error_msg = e.args[0] if e.args else "Validation error"
                    results["errors"].append({
                        "row": row_index + 1,
                        "data": row_data,
                        "error": error_msg
                    })
            return JsonResponse(results, status=200)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred during pandas processing: {str(e)}"}, status=500)


class ProductCategoryView:
    
    @csrf_exempt
    def category_collection_view(self, request):
        if request.method == 'GET':
            categories = category_service.get_all_categories()
            serializer = ProductCategorySerializer(categories, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)

        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
                category = category_service.create_new_category(data)
                return JsonResponse({"title": category.title}, status=201)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            except ValueError as e:
                return handle_value_error(e)

        return JsonResponse({"error": "Method not allowed"}, status=405)

    @csrf_exempt
    def category_detail_view(self, request, title):
        if request.method == 'GET':
            try:
                products = category_service.get_products_by_category(title)
                serializer = ProductSerializer(products, many=True)
                return JsonResponse(serializer.data, safe=False, status=200)
            except ValueError as e:
                return handle_value_error(e)

        elif request.method == 'PATCH':
            try:
                data = json.loads(request.body)
                category = category_service.update_existing_category(title, data)
                serializer = ProductCategorySerializer(category)
                return JsonResponse(serializer.data, status=200)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            except ValueError as e:
                return handle_value_error(e)

        elif request.method == 'DELETE':
            try:
                category_service.delete_category_record(title)
                return JsonResponse({"message": "Category deleted successfully."}, status=204)
            except ValueError as e:
                return handle_value_error(e)

        return JsonResponse({"error": "Method not allowed"}, status=405)
