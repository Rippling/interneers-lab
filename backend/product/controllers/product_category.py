from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from product.services.product_category import ProductCategoryService
from product.serializers.product_category import ProductCategorySerializer
from product.serializers.product import ProductSerializer
from product.pagination import StandardResultsSetPagination


class ProductCategoryViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductCategoryService()

    def list(self, request):
        categories = self.service.get_all_category()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(categories, request)
        if page is not None:
            serializer = ProductCategorySerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = self.service.create_category(serializer.validated_data)
                return Response(ProductCategorySerializer(category).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:  
            category = self.service.get_category(pk)
            serializer = ProductCategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = self.service.update_category(pk, serializer.validated_data)
                return Response(ProductCategorySerializer(category).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            self.service.delete_category(pk)
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])    
    def add_product(self, request, pk=None):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.service.add_product_to_category(pk, product_id)
            return Response({"message": "Product added to category."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'])
    def remove_product(self, request, pk=None):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.service.remove_product_from_category(pk, product_id)
            return Response({"message": "Product removed from category."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        try:
            products = self.service.list_products_in_category(pk)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
