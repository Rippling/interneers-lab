from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


# DRF automatically handles the GET/PUT/POST apis in this (recall all the code we had to write to manually make apis)

# Handles GET (list all) and POST (create new)
class ProductListCreateAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all() # The DB query to get everything
    serializer_class = ProductSerializer # The translator to use

# Handles GET (one item), PUT (update), and DELETE
class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    