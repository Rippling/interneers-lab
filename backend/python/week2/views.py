# view : code that runs when a client hits an endpoint i.e receives http request and decides what to do
# eg GET/products/, PUT/products/1

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer
from .store import product_store


class ProductListCreateAPIView(APIView):
    # list all product
    def get(self, request):
        products = product_store.list_all()
        # manual pagination
        page = request.query_params.get("page", "1")
        page_size = request.query_params.get("page_size", "5")
        if not page.isdigit() or not page_size.isdigit():
            return Response(
                {"error": "page and page_size must be integers"}, status=status.HTTP_400_BAD_REQUEST
            )

        page = int(page)
        page_size = int(page_size)
        if page <= 0 or page_size <= 0:
            return Response(
                {"error": "page and page_size must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST
            )

        total_items = len(products)
        start = (page-1)*page_size
        end = start + page_size
        paginated_products = products[start: end]
        product_data = []

        for product in paginated_products:
            product_data.append(product.to_dict())

        serializer = ProductSerializer(product_data, many=True)

        if end < total_items:
            next_page = page + 1
        else:
            next_page = None

        if page > 1:
            previous_page = page-1
        else:
            previous_page = None

        return Response(
            {
                "count": total_items,
                "page": page,
                "page_size": page_size,
                "next_page": next_page,
                "previous_page": previous_page,
                "results": serializer.data,
            }, status=status.HTTP_200_OK
        )

        # product_data = []
        # for product in products:
        #     product_data.append(product.to_dict())
        # # output serialisation
        # # without many = true DRF would expect one product
        # serializer = ProductSerializer(product_data, many=True)
        # # Response(product_data, status=status.HTTP_200_OK) is also valid
        # return Response(serializer.data, status=status.HTTP_200_OK)

    # create a product

    def post(self, request):
        # input serialisation
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = product_store.create(serializer.validated_data)
            response_serializer = ProductSerializer(product.to_dict())
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    # get specific product
    def get(self, request, product_id):
        product = product_store.get(product_id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductSerializer(product.to_dict())
            return Response(serializer.data, status=status.HTTP_200_OK)

    # update one product
    def put(self, request, product_id):
        existing_product = product_store.get(product_id)
        if not existing_product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND,)
        else:
            # validate new data first
            serializer = ProductSerializer(data=request.data)
            if (serializer.is_valid()):
                updated_product = product_store.update(
                    product_id, serializer.validated_data)
                response_serializer = ProductSerializer(
                    updated_product.to_dict())
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete data
    def delete(self, request, product_id):
        deleted = product_store.delete(product_id)
        if not deleted:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND,)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
