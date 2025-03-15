from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from .services import ProductService
from .serializers import ProductSerializer
from .models import Product
from .errorHandler import handle_exception

class ProductPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductCreate(APIView):
    def post(self, request):
        try:
            data = request.data
            result = ProductService.createProd(data)
            if not result["success"]:
                return Response({"error": result["data"]}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Product created successfully", "data": ProductSerializer(result["data"]).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return handle_exception(e)

class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        return ProductService.getAllProds()

class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get_object(self):
        prod_id = self.kwargs.get("id")
        prod = ProductService.getProdById(prod_id)
        if not prod:
            raise NotFound("Product not found") 
        return prod

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        try:
            prod_id = kwargs.get("id")
            updated_prod = ProductService.updateProd(prod_id, request.data)
            if not updated_prod:
                raise NotFound("Product not found") 
            return Response({"message": "Product Updated successfully", "data": ProductSerializer(updated_prod).data}, status=status.HTTP_200_OK)
        except Exception as e:
            return handle_exception(e)

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        try:
            prod_id = kwargs.get("id")
            success = ProductService.deleteProd(prod_id)
            if not success:
                raise Exception("Deletion failed")
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return handle_exception(e)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.exceptions import NotFound
# from .models import Product
# from .serializers import ProductSerializer
# from rest_framework import generics

# class ProductPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 100

# class ProductCreate(APIView):
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Product created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# class ProductList(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = ProductPagination

# class ProductDetail(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = "id"

#     def get_object(self):
#         try:
#             return super().get_object()
#         except Product.DoesNotExist:
#             raise NotFound({"error": "Product not found"})

# class ProductUpdate(generics.UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = "id"

#     def put(self, request, *args, **kwargs):
#         try:
#             return self.update(request, *args, **kwargs)
#         except Product.DoesNotExist:
#             raise NotFound({"error": "Product not found"})
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class ProductDelete(generics.DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = "id"

#     def delete(self, request, *args, **kwargs):
#         try:
#             return self.destroy(request, *args, **kwargs)
#         except Product.DoesNotExist:
#             raise NotFound({"error": "Product not found"})
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
