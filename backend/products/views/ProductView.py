from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from rest_framework.exceptions import ValidationError
from django.http import Http404

 
from ..services.ProductService import ProductService
from ..serializers import ProductSerializer
from ..models.ProductModel import Product
from ..errorHandler import handle_exception
from ..models.CategoryModel import ProductCategory

class ProductPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductCreate(APIView):
    def post(self, request):
        try:
            print("Received Data:", request.data)
            serializer = ProductSerializer(data=request.data)

            if serializer.is_valid():
                product = serializer.save()
                return Response(
                    {"message": "Product created successfully", "data": ProductSerializer(product).data},
                    status=status.HTTP_201_CREATED
                )
            else:
                print("Validation Errors:", serializer.errors)
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Exception Caught: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = ProductService.getAllProds()
        print(f"Queryset: {queryset}") 
        if queryset is None:
            return Product.objects.none() 
        return queryset

class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "id"

    def get_object(self):
        prod_id = self.kwargs.get("id")
        print(prod_id)
        prod = ProductService.getProdById(prod_id)
        if not prod:
            raise Http404("Product not found") 
        return prod


class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    
    def put(self, request, *args, **kwargs):
            try:
                prod_id = kwargs.get("id")
                result = ProductService.updateProd(prod_id, request.data)

                if result is None:
                    return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

                if isinstance(result, dict) and "errors" in result:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    "message": "Product updated successfully",
                    "data": ProductSerializer(result).data
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            prod_id = kwargs.get("id")
            updated_product = ProductService.updateProd(prod_id, request.data)

            if not updated_product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "message": "Product updated successfully",
                "data": ProductSerializer(updated_product).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
         
class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        try:
            prod_id = kwargs.get("id")
            success = ProductService.deleteProd(prod_id)
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except (NotFound, Http404) as nf:
            return Response({"error": str(nf)}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AddCategoryToProduct(generics.UpdateAPIView):
   
    def put(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        category_id = kwargs.get("category_id")

        try:
            response_data = ProductService.add_category_to_product(product_id, category_id)

            if response_data.get("status") == 400:
                return Response({"error": response_data.get("message")}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": response_data.get("message")}, status=status.HTTP_200_OK)

        except (NotFound, Http404) as nf:  # ✅ Catch both DRF and Django NotFound
            return Response({"error": str(nf)}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveCategoryFromProduct(generics.UpdateAPIView):
  
    def put(self, request, *args, **kwargs):
        try:
            product_id = kwargs.get("product_id")
            category_id = kwargs.get("category_id")
            response = ProductService.remove_category_from_product(product_id, category_id)
            return Response({"message": response["message"]}, status=response["status"])
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)