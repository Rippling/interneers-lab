from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer


products=[
    {"id":1,"name":"product1","price":100},
    {"id":2,"name":"product2","price":200},
]

# Create your views here.
class ProductViewSet(viewsets.ViewSet):

    def list(self,request):
        return Response(products)
    
    def create(self,request):
        data=request.data
        serilizer=ProductSerializer(data=data)
       
        
        if serilizer.is_valid(): # this is necessary to validate the data before saving/creating it
           
            products.append(serilizer.validated_data) # this is used when the serializer is a normal serializer(not model serializer)
            # products.append(serilizer.data) //this is used when the serializer is a model serializer
            return Response(serilizer.validated_data,status=status.HTTP_201_CREATED)
        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self,request,pk=None):
        try:
            pk=int(pk)
        except ValueError:
            return Response({"error":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)
        for product in products:
            if product['id']==pk:
                return Response(product)
        return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
    
    def update(self,request,pk=None):

        try:
            pk=int(pk)
        except ValueError:
            return Response({"error":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)
        

        for product in products:
            if product['id']==pk:
                product.update(request.data)
                return Response(product,status=status.HTTP_200_OK)
        return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self,request,pk=None):
        
        try:
            pk=int(pk)
        except ValueError:
            return Response({"error":"Invalid ID"},status=status.HTTP_400_BAD_REQUEST)
        
        for product in products:
            if product['id']==pk:
                products.remove(product)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error":"Product not found"},status=status.HTTP_404_NOT_FOUND)
    
    
         
