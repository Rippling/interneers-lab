from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from products.serializers import ProductSerializer
from products.services.product_service import ProductService


class ProductPagination(PageNumberPagination):
    page_size = 2  # Set the number of products per page
    page_size_query_param = "page_size"


product_service = ProductService()


@api_view(["GET", "POST"])
def productsView(request):
    if request.method == "GET":
        try:
            sort_by = request.query_params.get("sort_by")
            filters = {}

            # Extract and validate category
            category = request.query_params.get('category')
            if category and category.strip():
                filters['category'] = category.strip()

            # Extract name filter
            name = request.query_params.get('name')
            if name and name.strip():
                filters['name'] = name.strip()

            # Extract brand filter
            brand = request.query_params.get('brand')
            if brand and brand.strip():
                filters['brand'] = brand.strip()

            # Extract min_price filter
            min_price = request.query_params.get('min_price')
            if min_price and min_price.strip():
                filters['min_price'] = min_price.strip()

            # Extract max_price filter
            max_price = request.query_params.get('max_price')
            if max_price and max_price.strip():
                filters['max_price'] = max_price.strip()

            products = product_service.get_all_products(sort_by=sort_by, filters=filters)

            paginator = ProductPagination()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            try:
                product = product_service.create_product(serializer.validated_data)
                return Response(
                    ProductSerializer(product).data, status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET", "PUT", "DELETE"])
def productDetailView(request, id):
    try:
        if request.method == "GET":
            product = product_service.get_product_by_id(id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "PUT":
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product = product_service.update_product(id, serializer.validated_data)
                return Response(
                    ProductSerializer(product).data, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif request.method == "DELETE":
            product_service.delete_product(id)
            return Response(
                {"message": "Product deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )

    except ValueError as e:
        if "No product with id" in str(e):
            return Response(
                {"error": "Product not found", "details": str(e)},
                status=status.HTTP_404_NOT_FOUND,
            )
        elif "Invalid ObjectId format" in str(e):
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
