from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime

from .serializers import CategorySerializer, ProductSerializer
from .service import CategoryService, ProductService
from .models import Category, Product

# Create your views here.

class CategoryViewSet(viewsets.ViewSet):
    lookup_field = 'slug'

    def list(self, request):
        categories = CategoryService.list_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        category = CategoryService.get_category_by_slug(slug)
        if not category:
            return Response(
                {'error': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            category = CategoryService.create_category(data)
            return Response(
                CategorySerializer(category).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, slug=None):
        category = CategoryService.get_category_by_slug(slug)
        if not category:
            return Response(
                {'error': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CategorySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            category.name = data.get('name', category.name)
            category.description = data.get('description', category.description)
            category.updated_at = datetime.utcnow()
            category.save()
            return Response(CategorySerializer(category).data)
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, slug=None):
        category = CategoryService.get_category_by_slug(slug)
        if not category:
            return Response(
                {'error': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if there are associated products
        products = Product.objects(category=category)
        if products:
            return Response(
                {'error': 'Cannot delete category with associated products'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        CategoryService.delete_category(category)
        return Response(
            {'message': f'Category "{category.name}" was successfully deleted'},
            status=status.HTTP_200_OK
        )

class ProductViewSet(viewsets.ViewSet):
    lookup_field = 'slug'

    def list(self, request):
        # Base queryset
        filters = {}
        
        # Filter by category
        category_slug = request.query_params.get('category', None)
        if category_slug:
            category = CategoryService.get_category_by_slug(category_slug)
            if category:
                filters['category'] = category
        
        # Filter by price range
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        if min_price:
            filters['price__gte'] = float(min_price)
        if max_price:
            filters['price__lte'] = float(max_price)
            
        # Filter by stock status
        stock_status = request.query_params.get('stock_status', None)
        if stock_status:
            products = ProductService.filter_products_by_stock(stock_status)
        else:
            # Filter by product status
            product_status = request.query_params.get('status', None)
            if product_status:
                filters['status'] = product_status
            
            # Get filtered products
            products = ProductService.list_products(filters)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        product = ProductService.get_product_by_slug(slug)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        # Add category_name for serializer
        product_data = ProductSerializer(product).data
        product_data['category_name'] = product.category.name if product.category else ''
        return Response(product_data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Handle category reference
            category_id = data.pop('category', None)
            category = CategoryService.get_category_by_id(category_id)
            if not category:
                # Try by slug
                category = CategoryService.get_category_by_slug(category_id)
            
            if not category:
                return Response(
                    {'error': 'Invalid category'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            data['category'] = category
            
            try:
                product = ProductService.create_product(data)
                product_data = ProductSerializer(product).data
                product_data['category_name'] = category.name
                return Response(
                    product_data,
                    status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, slug=None):
        product = ProductService.get_product_by_slug(slug)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ProductSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = serializer.validated_data
            
            # Handle category update if present
            if 'category' in data:
                category_id = data.pop('category')
                category = CategoryService.get_category_by_id(category_id)
                if not category:
                    # Try by slug
                    category = CategoryService.get_category_by_slug(category_id)
                
                if category:
                    data['category'] = category
                else:
                    return Response(
                        {'error': 'Invalid category'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Update the timestamp
            data['updated_at'] = datetime.utcnow()
            
            try:
                updated_product = ProductService.update_product(product, data)
                product_data = ProductSerializer(updated_product).data
                product_data['category_name'] = updated_product.category.name if updated_product.category else ''
                return Response(product_data)
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, slug=None):
        product = ProductService.get_product_by_slug(slug)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        ProductService.delete_product(product)
        return Response(
            {'message': f'Product "{product.name}" was successfully deleted'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = Product.objects(featured=True)
        serializer = ProductSerializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_products = ProductService.filter_products_by_stock('low_stock')
        serializer = ProductSerializer(low_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_stock(self, request, slug=None):
        product = ProductService.get_product_by_slug(slug)
        if not product:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            quantity = int(request.data.get('quantity', 0))
            if quantity < 0:
                return Response(
                    {'error': 'Quantity cannot be negative'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product.quantity = quantity
            product.updated_at = datetime.utcnow()
            product.save()
            
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except (TypeError, ValueError):
            return Response(
                {'error': 'Invalid quantity value'},
                status=status.HTTP_400_BAD_REQUEST
            )
