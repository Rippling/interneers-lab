from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from bson import ObjectId
from mongoengine.errors import DoesNotExist

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
            data = request.data.copy()
            print("Received Data:", data)

            categories = ProductCategory.objects.filter(title__in=data["category"])

            if not categories:
                return Response({"error": "One or more categories not found"}, status=status.HTTP_400_BAD_REQUEST)

            print(f"Resolved Category IDs: {[str(cat.id) for cat in categories]}")

            product = Product(
                name=data["name"],
                description=data.get("description", ""),
                brand=data.get("brand", ""),
                category=list(categories),  
                price=data["price"],
                quantity=data["quantity"]
            )

            product.save()

            saved_product = Product.objects.get(id=product.id)
            # print(f"Product Categories After Save: {[cat.title for cat in saved_product.category]}")

            return Response(
                {"message": "Product created successfully", "data": ProductSerializer(saved_product).data},
                status=status.HTTP_201_CREATED
            )

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
        

class AddCategoryToProduct(generics.UpdateAPIView):
   
    def put(self, request, *args, **kwargs):
        try:
           
            product_id = kwargs.get("product_id")
            category_id = kwargs.get("category_id")

            response = ProductService.add_category_to_product(product_id, category_id)
            return Response(response, status=response["status"])

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