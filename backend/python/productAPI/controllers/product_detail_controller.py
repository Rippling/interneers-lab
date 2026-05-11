from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productAPI.services import ProductService
from productAPI.serializers import ProductSerializer

class ProductDetailController(APIView):
    
    def get(self, request, product_id):
        product = ProductService.list_single_product(product_id)
        
        if not product:
            return Response({"error":"Product not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def put(self, request, product_id):
        serializer = ProductSerializer(data=request.data)
        
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        updated_product = ProductService.update_product(
            product_id,
            serializer.validated_data
        )
        
        if not updated_product:
            return Response(
                {"error": "Product not found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(ProductSerializer(updated_product).data, status=status.HTTP_202_ACCEPTED)
    
    
    
    def delete(self, request, product_id):
        deleted = ProductService.delete_product(product_id)
        
        if not deleted:
            return Response(
                {"error":"Product Not Found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            {"message":"Delete Successful!"},
            status=status.HTTP_204_NO_CONTENT
        )