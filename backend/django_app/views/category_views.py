from rest_framework import viewsets, status, pagination
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from bson import ObjectId
from django_app.serializers.category_serializer import CategorySerializer
from django_app.services.category_service import CategoryService
from django_app.services.product_service import ProductService
from datetime import datetime
from django_app.views.product_views import ProductViewSet


class CategoryPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20
    
class CategoryViewSet(viewsets.ViewSet):

    paginator_class = CategoryPagination

    def create(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                response = CategoryService.create_category(serializer.validated_data)
                return Response(
                    {
                        "message": "Category created successfully",
                        "created_category": response
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Validation error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ParseError as e:
            return Response(
                {"error": "Invalid JSON format", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def list(self, request):
        try:
            ordering = request.query_params.get('ordering')

            created_after = request.query_params.get('created_after')
            created_before = request.query_params.get('created_before')
            updated_after = request.query_params.get('updated_after')
            updated_before = request.query_params.get('updated_before')

            filters = {}
            date_format = "%Y-%m-%d"

            try:
                if created_after:
                    filters['created_after'] = datetime.strptime(created_after, date_format)
                if created_before:
                    filters['created_before'] = datetime.strptime(created_before, date_format)
                if updated_after:
                    filters['updated_after'] = datetime.strptime(updated_after, date_format)
                if updated_before:
                    filters['updated_before'] = datetime.strptime(updated_before, date_format)
            except ValueError:
                return Response(
                    {"error": "Invalid date format", "message": f"Dates must be in format YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            categories = CategoryService.get_all_categories(ordering=ordering, filters=filters)
            paginator = self.paginator_class()
            page_size = request.query_params.get('page_size', paginator.page_size)
            try:
                page_size = int(page_size)
                if page_size <= 0:
                    return Response(
                        {
                            "error": "Invalid page size",
                            "message": f"Page size cannot be less than or equal to 0."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if page_size>paginator.max_page_size:
                    return Response(
                    {
                        "error": "Invalid page size",
                        "message": f"Page size cannot exceed {paginator.max_page_size}."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValueError:
                return Response(
                    {"error": "Invalid page size", "message": "Page size must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            paginated_categories = paginator.paginate_queryset(categories, request)
            return paginator.get_paginated_response(paginated_categories)
        except NotFound:
            return Response(
                {"error": "Invalid page", "message": "Requested page is out of range."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def retrieve(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid category ID", "message": "Category ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            category = CategoryService.get_category_by_id(ObjectId(pk))
            if not category:
                return Response(
                    {"error": "Category not found", "message": f"No category found with ID {pk}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(category)
        except Exception as e:
            return Response({"error": "Something went wrong", "message": str(e)})
        
    def update(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid category ID", "message": "Category ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                ) 
            existing_category = CategoryService.get_category_by_id(ObjectId(pk))
            if not existing_category:
                return Response(
                        {"error": "Category not found", "message": f"No category found with ID {pk}."},
                        status=status.HTTP_404_NOT_FOUND
                ) 
            serializer = CategorySerializer(instance=existing_category, data=request.data)
            if serializer.is_valid():
                updated_category = CategoryService.update_category(serializer.validated_data, ObjectId(pk))
                return Response(
                    {
                        "message": "Category updated successfully",
                        "updated_category": CategorySerializer(updated_category).data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Validation error", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ParseError as e:
            return Response(
                {"error": "Invalid JSON format", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def destroy(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid category ID", "message": "Category ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                ) 
            category = CategoryService.get_category_by_id(ObjectId(pk))
            if not category:
                return Response(
                        {"error": "Category not found", "message": f"No category found with ID {pk}."},
                        status=status.HTTP_404_NOT_FOUND
                ) 
            category_title = category["title"]
            CategoryService.delete_category(ObjectId(pk))
            return Response(
                {"message": f"Category '{category_title}' deleted successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": "Something went wrong", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def list_products(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid category ID", "message": "Category ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            category = CategoryService.get_category_by_id(ObjectId(pk))
            if not category:
                return Response(
                    {"error": "Category not found", "message": f"No category found with ID {pk}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            products = ProductService.get_products_by_category(ObjectId(pk))
            paginator = self.paginator_class()
            page_size = request.query_params.get('page_size', paginator.page_size)
            try:
                page_size = int(page_size)
                if page_size>paginator.max_page_size:
                    return Response(
                    {
                        "error": "Invalid page size",
                        "message": f"Page size cannot exceed {paginator.max_page_size}."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValueError:
                return Response(
                    {"error": "Invalid page size", "message": "Page size must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            paginated_categories = paginator.paginate_queryset(products, request)
            paginated_response = paginator.get_paginated_response(paginated_categories).data
            for product in paginated_response["results"]:
                product.pop("category", None)
            final_response = {
                "category": category,
                **paginated_response
            }
            return Response(final_response)
        except Exception as e:
            return Response(
                {"error": "Server error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def add_product(self, request, pk=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid category ID", "message": "Category ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            category = CategoryService.get_category_by_id(ObjectId(pk))
            if not category: 
                return Response(
                    {"error": "Category not found", "message": f"No category found with ID {pk}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            request.data["category"] = category["title"]
            return ProductViewSet().create(request)
        except Exception as e:
            return Response(
                {"error": "Server error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def remove_product(self, request, pk=None, product_id=None):
        try:
            if not ObjectId.is_valid(pk):
                return Response(
                    {"error": "Invalid category ID", "message": "Category ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            category = CategoryService.get_category_by_id(ObjectId(pk))
            if not category: 
                return Response(
                    {"error": "Category not found", "message": f"No category found with ID {pk}."},
                    status=status.HTTP_404_NOT_FOUND
                )
            if not ObjectId.is_valid(product_id):
                return Response(
                    {"error": "Invalid product ID", "message": "Product ID must be a 24-character hex string."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product = ProductService.get_product_by_id(ObjectId(product_id))
            if not product or product["category"]!=category["title"]:
                return Response(
                    {"error": "Product not found", "message": f"No product found with ID {pk} in '{category['title']}' category."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return ProductViewSet().destroy(None, product_id)
        except Exception as e:
            return Response(
                {"error": "Server error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

