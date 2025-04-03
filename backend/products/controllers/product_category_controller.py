from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from ..serializers import ProductCategorySerializer
from ..services.product_category_service import ProductCategoryService

class CategoryPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100

service = ProductCategoryService()

@api_view(["GET", "POST"])
def productCategoryView(request):
    """Handle categories list operations"""
    if request.method == "GET":
        try:
            
            categories = service.get_all_categories()
            
            paginator = CategoryPagination()
            result_page = paginator.paginate_queryset(categories, request)
            serializer = ProductCategorySerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == "POST":
        serializer = ProductCategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            category = service.create_category(serializer.validated_data)
            return Response(
                ProductCategorySerializer(category).data,
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def productCategoryDetailView(request, id):
    """Handle single category operations"""
    try:
        if request.method == "GET":
            category = service.get_category_by_id(id)
            return Response(ProductCategorySerializer(category).data)

        elif request.method == "PUT":
            
            serializer = ProductCategorySerializer(data=request.data, partial=True)  # only provided fields will be updated
            if not serializer.is_valid(): 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            category = service.update_category(id, serializer.validated_data)
            return Response(ProductCategorySerializer(category).data)

        elif request.method == "DELETE":
            service.delete_category(id)
            return Response(status=status.HTTP_204_NO_CONTENT)

    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(
            {"error": "Server error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )