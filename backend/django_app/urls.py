from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from .product_api import ProductAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, List

products: Dict[int, dict] = {}
product_id_counter = 1

class ProductAPIView(APIView):
    def get(self, request):
        pv = list(products.values())
        limit = int(request.query_params.get('limit', 10))
        pv_top10 = []
        for i in range(0, limit):
            pv_top10.append(pv[i])
        return Response(pv_top10)
    
    def post(self, request):
        global product_id_counter
        product = {
            'id': product_id_counter,
            'name': request.data['name'],
            'price': float(request.data['price']),
            'description': request.data.get('description')
        }
        products[product_id_counter] = product
        product_id_counter += 1
        return Response(product, status=status.HTTP_201_CREATED)


def hello_world(request):
    return HttpResponse("Hello, world! This is our interneers-lab Django server.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
    path('products/', ProductAPIView.as_view(), name='products'),
]
