from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from rest_framework.pagination import PageNumberPagination
from .serializers import ProductSerializer
from mongoengine.errors import DoesNotExist, ValidationError


class ProductPagination(PageNumberPagination):
    page_size = 2  # Set the number of products per page
    page_size_query_param = "page_size"


@api_view(["GET", "POST"])
def productsView(request):
    if request.method == "GET":
        paginator = ProductPagination()
        products = Product.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def productDetailView(request, id):
    try:
        product = Product.objects.get(id=id)
    except DoesNotExist:
        return Response(
            {
                "error": "Product not found",
                "details": f"No product with id {id} exists.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValidationError:
        return Response(
            {"error": "Invalid ObjectId format"}, status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif request.method == "DELETE":
        product.delete()
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
