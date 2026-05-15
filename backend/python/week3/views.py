# same as week 2, only request passes through service rather than directly to store
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .service import product_service


class ProductListCreateAPIView(APIView):
    # list all product
    def get(self, request):
        products = product_service.list_all()
        product_data = []
        for product in products:
            product_data.append(product.to_dict())

        serializer = ProductSerializer(product_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create a product
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = product_service.create(serializer.validated_data)
            response_serializer = ProductSerializer(product.to_dict())
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    # get one product
    def get(self, request, id):
        product = product_service.get(id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductSerializer(product.to_dict())
            return Response(serializer.data, status=status.HTTP_200_OK)

    # update one product
    def put(self, request, id):
        existing_product = product_service.get(id)
        if not existing_product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                updated_product = product_service.update(
                    id, serializer.validated_data)
                response_serializer = ProductSerializer(
                    updated_product.to_dict())
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete product
    def delete(self, request, id):
        deleted = product_service.delete(id)
        if not deleted:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
