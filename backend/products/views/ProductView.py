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

            category_obj = ProductCategory.objects(title=data["category"]).first()

            if not category_obj:
                return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

            data["category"] = category_obj.id  
            print(f"Resolved Category ID: {data['category']}") 

            product = Product(
                name=data["name"],
                description=data.get("description", ""),
                brand=data.get("brand", ""),
                category=category_obj,  
                price=data["price"],
                quantity=data["quantity"]
            )
            product.save()  

            return Response(
                {"message": "Product created successfully", "data": ProductSerializer(product).data},
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

class CheckCategoryView(generics.RetrieveAPIView):
    def get(self, request):
        category_exists = ProductCategory.objects.filter(title="c").first()
        
        print(ProductCategory.objects.filter(title="c").first())
        if category_exists:
            return Response({"message": "Category exists", "category": category_exists.title})
        return Response({"message": "Category does not exist"})
    
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

# class AddToCategory(generics.UpdateAPIView):
    
