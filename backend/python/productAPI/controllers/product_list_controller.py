from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productAPI.services import ProductService
from productAPI.serializers import ProductSerializer
from productAPI.serializers import ProductFilterSerializer

class ProductListController(APIView):
    
    def get(self, request):
        
        filters={}
        serializer = ProductFilterSerializer(data = request.query_params)
            
        serializer.is_valid(raise_exception=True)
        
        filters = serializer.validated_data
            
        products = ProductService.list_products(filters)
        
        
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data) #this ones to valiidate json
        
        if serializer.is_valid():
            product = ProductService.create_product(serializer.validated_data)
            return Response(
                ProductSerializer(product).data, #this to convert object to json
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    