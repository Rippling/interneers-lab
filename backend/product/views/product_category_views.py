from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from product.serializers.category_serializer import ProductCategorySerializer
from product.services.product_category_service import ProductCategoryService

class ProductCategoryView(APIView):
    def __init__(self):
        self.category_service = ProductCategoryService()

    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)

        if serializer.is_valid():
            category = self.category_service.create_category(serializer.validated_data)
            return Response(ProductCategorySerializer(category).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        categories = self.category_service.get_all_categories()
        return Response(ProductCategorySerializer(categories, many=True).data, status=status.HTTP_200_OK)


class SingleProductCategoryView(APIView):
    def __init__(self):
        self.category_service = ProductCategoryService()

    def get(self, request, category_id):
        category = self.category_service.get_category_by_id(category_id)
        if category:
            return Response(ProductCategorySerializer(category).data, status=status.HTTP_200_OK)
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, category_id):
        category = self.category_service.get_category_by_id(category_id)
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            updated_category = self.category_service.update_category(category_id, serializer.validated_data)
            return Response(ProductCategorySerializer(updated_category).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        success = self.category_service.delete_category(category_id)
        if success:
            return Response({"message": "Category deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
