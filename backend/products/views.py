from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer

# In-memory storage for products
products_list = []
product_id_counter = 1

class ProductPagination(PageNumberPagination):
    page_size = 2  # Set the number of products per page
    page_size_query_param = 'page_size'
    

@api_view(['GET', 'POST'])
def productsView(request):
    global product_id_counter 

    if request.method == 'GET':
        paginator = ProductPagination()
        result_page = paginator.paginate_queryset(products_list, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product_data = serializer.validated_data
            product_data['id'] = product_id_counter 
            product_id_counter += 1
            products_list.append(product_data)
            return Response(product_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def productDetailView(request, id):
    global products_list

    product = next((p for p in products_list if p['id'] == id), None)

    if product is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product.update(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        products_list = [p for p in products_list if p['id'] != id]
        return Response(status=status.HTTP_204_NO_CONTENT)
