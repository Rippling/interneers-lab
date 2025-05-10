# from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_mongoengine.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from products.serializers import ProductSerializer, ProductCategorySerializer
from products.services import ProductService, ProductCategoryService
from products.models import ProductCategory, Products


class ProductView(ListCreateAPIView):

    #queryset = ProductService.list_products()
    #queryset = Products.objects.all()
    serializer_class = ProductSerializer
    

    def get_queryset(self):
        return ProductService.list_products()


    def create(self, request, *args, **kwargs):
        # Custom product creation logic (if needed)
        print("request Data", request.data)
        return super().create(request, *args, **kwargs)


    # def get_queryset(self):
    #     return ProductService.list_products()

    # def create(self, request, *args, **kwargs):
    #     product = ProductService.create_product(request.data)
    #     serializer = self.get_serializer(product)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(RetrieveUpdateDestroyAPIView):

    #queryset = ProductService.list_products()
    #queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'       # The field in your model
    lookup_url_kwarg = 'product_id'

    def get_queryset(self):
        return ProductService.list_products()


    # def get_object(self):
    #     return ProductService.retrieve_product(self.kwargs.get(self.lookup_url_kwarg))

    # def update(self, request, *args, **kwargs):
    #     updated_product = ProductService.update_product(self.kwargs.get(self.lookup_url_kwarg), request.data)
    #     serializer = self.get_serializer(updated_product)
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     deleted_product = ProductService.delete_product(self.kwargs.get(self.lookup_url_kwarg))
    #     serializer = self.get_serializer(deleted_product)
    #     return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class ProductCategoryView(ListCreateAPIView):
    #queryset = ProductCategoryService.list_products()
    #queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer



    def get_queryset(self):
         return ProductCategoryService.list_categories()

    # def create(self, request, *args, **kwargs):
    #     product = ProductCategoryService.create_product(request.data)
    #     serializer = self.get_serializer(product)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductsByCategoryView(APIView):

    def get(self, request, category_id):
        try:
            category = ProductCategoryService.retrieve_category(category_id=category_id)
            #category = ProductCategory.objects.get(category_Id=category_id)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        
        products = ProductCategoryService.filter_products_by_category(category=category)
        #products = Products.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, category_id):
        try:
            category = ProductCategoryService.retrieve_category(category_id=category_id)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        data_with_category = request.data.copy()
        data_with_category['category_Id'] = category_id

        serializer = ProductSerializer(data=data_with_category)
        
        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, category_id):
        try:
            ProductCategoryService.delete_category(category_id=category_id)
        except ProductCategory.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)

    



# class ProductView(generics.ListCreateAPIView):
    
#     serializer_class = ProductSerializer
    
#     def get_queryset(self):
#         return Products.objects()
    

# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    
#     serializer_class = ProductSerializer
#     lookup_field = 'int_id'  # Specify the field to look up by (default is 'pk')
#     lookup_url_kwarg = 'int_id'  # Specify the keyword argument for the lookup field

#     def get_object(self):
#         id = self.kwargs.get(self.lookup_url_kwarg)
#         return Products.objects.get(int_id=id)

#     def get_queryset(self):
#         return Products.objects.all()



# Create your views here.
# class ProductViewSet(viewsets.ViewSet):

#     def list(self,request):
#         return Response(products)
    
#     def create(self,request):
#         data=request.data
#         serilizer=ProductSerializer(data=data)
       
        
#         if serilizer.is_valid(): # this is necessary to validate the data before saving/creating it
           
#             products.append(serilizer.validated_data) # this is used when the serializer is a normal serializer(not model serializer)
#             # products.append(serilizer.data) //this is used when the serializer is a model serializer
#             return Response(serilizer.validated_data,status=status.HTTP_201_CREATED)
#         return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#     def retrieve(self,request,pk=None):
#         try:
#             pk=int(pk)
#         except ValueError:
#             return Response({"error":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)
#         for product in products:
#             if product['id']==pk:
#                 return Response(product)
#         return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
    
#     def update(self,request,pk=None):

#         try:
#             pk=int(pk)
#         except ValueError:
#             return Response({"error":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)
        

#         for product in products:
#             if product['id']==pk:
#                 product.update(request.data)
#                 return Response(product,status=status.HTTP_200_OK)
#         return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
    
#     def destroy(self,request,pk=None):
        
#         try:
#             pk=int(pk)
#         except ValueError:
#             return Response({"error":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)
        
#         for product in products:
#             if product['id']==pk:
#                 products.remove(product)
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
    
    
         
