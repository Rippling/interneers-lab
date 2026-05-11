from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productAPI.services import ProductCategoryService
from productAPI.serializers import ProductCategorySerializer

class ProductCategoryDetailController(APIView):
    
    def put(self, request, category_id):
        serializer = ProductCategorySerializer(data = request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        updated_category = ProductCategoryService.update_category(category_id, serializer.validated_data)
        
        if not updated_category:
            return Response(
                {"error": "Category not found!"},
                status=status.HTTP_404_NOT_FOUND
            ) 
        
        return Response(ProductCategorySerializer(updated_category).data, status=status.HTTP_202_ACCEPTED)
    
    

    def delete(self, request, category_id):
        deleted = ProductCategoryService.delete_category(category_id)
        
        if not deleted:
            return Response(
                {"error":"Category Not Found!"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )