from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from .services import ProductService

class ProductController(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        try:
            product = ProductService.create_product(request.data)
            print("Product instance created:", product, type(product))
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            print("Product instance created:", product, type(product))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, product_id=None):
        if product_id:
            product = ProductService.get_product_by_id(product_id)
            if product:
                return Response(ProductSerializer(product).data)
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        products = Product.objects.all()
        return Response(ProductSerializer(products, many=True).data)

    def put(self, request, product_id):
        updated_product = ProductService.update_product(product_id, request.data)
        if updated_product:
            return Response(ProductSerializer(updated_product).data)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        success = ProductService.delete_product(product_id)
        if success:
            return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Product not found at views"}, status=status.HTTP_404_NOT_FOUND)
