from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .pagination import ProductPagination
from .services import ProductService
from rest_framework.generics import ListAPIView

class ProductListCreateView(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return ProductService.list_products()

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = ProductService.create_product(serializer.validated_data)
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": "Failed to create product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = ProductService.get_product(product_id)
        if product:
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = ProductService.update_product(product_id, serializer.validated_data)
                if product:
                    return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": "Failed to update product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Validation failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            if ProductService.delete_product(product_id):
                return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Failed to delete product", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)