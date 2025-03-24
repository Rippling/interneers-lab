from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, List

products: Dict[int, dict] = {}
product_id_counter = 1

class ProductAPIView(APIView):
    def get(self, request):
        product_values = list(products.values())
        limit = int(request.query_params.get('limit', 10))
        product_values_top10 = []
        for i in range(0, limit):
            product_values_top10.append(product_values[i])
        return Response(product_values_top10)
    
    def post(self, request):
        global product_id_counter

        if not request.data.get('name') or not request.data.get('price'):
            return Response(
                {'error': 'Name and price are required fields'},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = {
            'id': product_id_counter,
            'name': request.data['name'],
            'price': float(request.data['price']),
            'description': request.data.get('description', '')
        }
        products[product_id_counter] = product
        product_id_counter += 1
        return Response(product, status=status.HTTP_201_CREATED)