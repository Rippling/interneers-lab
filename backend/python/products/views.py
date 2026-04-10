from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .services import product_service,category_service
import csv,io

@api_view(['GET', 'POST'])
def product_list_controller(request):
   
    if request.method == 'GET':
        raw_filters = {
            'min_price': request.query_params.get('min_price'),
            'max_price': request.query_params.get('max_price'),
            'brand': request.query_params.get('brand'),
        }
        categories = request.query_params.getlist('category')
        if categories:
            raw_filters['categories'] = categories
        
        clean_filters = {key: value for key, value in raw_filters.items() if value is not None}
        
        products = product_service.get_all_products(clean_filters)
        
        products_json = [json.loads(product.to_json()) for product in products]
        
        return Response(products_json, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        incoming_data = request.data 
        
        new_product = product_service.create_product(incoming_data)
        
        product_json = json.loads(new_product.to_json())
        return Response(product_json, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'POST'])
def category_list_controller(request):
    
    if request.method == 'GET':
        categories = category_service.get_all_categories()
        categories_json = json.loads(categories.to_json())
        return Response(categories_json, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        incoming_data = request.data 
        new_category = category_service.create_category(incoming_data)
        category_json = json.loads(new_category.to_json())
        return Response(category_json, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def category_products_controller(request, category_id):
    if request.method == 'GET':
        products = product_service.get_products_by_category(category_id=category_id)
        products_json = json.loads(products.to_json())
        print(category_id)
        return Response(products_json, status=status.HTTP_200_OK)
    
@api_view(['PUT', 'PATCH'])
def product_detail_controller(request, product_id):
    if request.method in ['PUT', 'PATCH']:
        incoming_data = request.data
        
        updated_product = product_service.update_product(product_id, incoming_data)
        if "error" in updated_product:
            return Response({"error": "category not found"}, status=status.HTTP_400_BAD_REQUEST)
        if updated_product:
            product_json = json.loads(updated_product.to_json())
            return Response(product_json, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
@api_view(['POST'])
def bulk_create_products(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return Response(
                {"error": "Please upload a CSV file with the form key 'file'."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        csv_file = request.FILES['file']

        if not csv_file.name.endswith('.csv'):
            return Response(
                {"error": "Invalid file type. Please upload a .csv file."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            
            reader = csv.DictReader(io_string)
            products_data = []
            
            for row in reader:
                cleaned_row = {key.strip(): value.strip() for key, value in row.items() if value.strip()}
                products_data.append(cleaned_row)

            result = product_service.bulk_create_products(products_data)

            if "error" in result:
                return Response(
                    {"error": result["error"]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {"message": f"Successfully uploaded {result['count']} products from CSV!"}, 
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"error": f"Error parsing CSV: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )