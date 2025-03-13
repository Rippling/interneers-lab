from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .services import ProductService
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Product

class ProductPagination(PageNumberPagination):

    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductCreate(APIView):

    def Post(self, request):
        data = request.data
        data1 = ProductService.createProd(data)
        return Response({"message" : "Product created successfully", "data": ProductSerializer(data1).data} , status = status.HTTP_201_CREATED)


class ProductList(generics.ListAPIView):

    queryset= ProductService.getAllProds()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductDetail(generics.RetrieveAPIView):

    serializer_class = ProductSerializer
    lookup_field = "id"
    
    def get_object(self):

        prod_id = self.kwargs.get("id")
        prod = ProductService.getProdById(prod_id)
        print(f"Product Retrieved: {prod}")
        return prod


class ProductUpdate(generics.UpdateAPIView):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

    def put(self , request, *args, **kwargs):
        prod_id = kwargs.get("id")
        updated_prod = ProductService.updateProd(prod_id, request.data)
        return Response({"message": "Product Updated successfully" , "data" : ProductSerializer(updated_prod).data} , status= status.HTTP_200_OK)


class ProductDelete(generics.DestroyAPIView):

    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    lookup_field = "id"

    def delete(self , request, *args, **kwargs):
        prod_id = kwargs.get("id")
        resp = ProductService.deleteProd(prod_id)
        return Response({"mesage": "Product deleted successfully" } , status= status.HTTP_204_NO_CONTENT)



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
