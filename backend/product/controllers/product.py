from rest_framework import viewsets, status
from rest_framework.response import Response
from product.services.product import ProductService
from product.serializers.product import ProductSerializer
from product.pagination import StandardResultsSetPagination
from mongoengine import Q


class ProductViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    def list(self, request):
        products = self.service.get_all_products()

        # Apply filteration by categories if provided in query parameters.
        # Example: ?category=60e7a5e12f1a2c3b456789ab&category=60e7a5e12f1a2c3b456789ac
        category_ids = request.query_params.getlist('category')
        if category_ids:
            products = products.filter(category__in=category_ids)

        # Apply search filter (e.g., search by product name or brand)
        # Example: ?search=iphone
        search_query = request.query_params.get('search')
        if search_query:
            products = products.filter(Q(name__icontains=search_query) | Q(brand__icontains=search_query))

        # Apply ordering if specified
        # Example: ?ordering=price or ?ordering=-price for descending order
        ordering = request.query_params.get('ordering')
        if ordering:
            products = products.order_by(ordering)

        # Instantiate the paginator
        paginator = StandardResultsSetPagination()
        # Paginate the queryset
        page = paginator.paginate_queryset(products, request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def  create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product=self.service.create_product(serializer.validated_data)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            product = self.service.get_product(pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = self.service.update_product(pk, serializer.validated_data)
                return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            self.service.delete_product(pk)
            return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
