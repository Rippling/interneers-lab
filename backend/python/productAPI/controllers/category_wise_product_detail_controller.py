from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from productAPI.services import ProductCategoryService, ProductService
from productAPI.serializers import ProductSerializer

class CategoryWiseProductDetailController(APIView):
    
    def delete(self, request, category_id, product_id):
        result = ProductService.unassign_category(product_id,category_id)
        if not result:
            return Response(
                {
                    "error":"No product found with the given ID"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {
                "message":"Successfully removed product from this category"
            },
            status=status.HTTP_204_NO_CONTENT
        )