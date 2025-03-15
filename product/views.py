from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer,ProductHistorySerializer
from .services import ProductService
from .models import ProductHistory
from rest_framework.pagination import PageNumberPagination
from datetime import datetime,timezone,timedelta
import decimal

# PRODUCTS = {}                   #creating python dict for storing products for in memory operations
# NEXT_ID = 1

# # basic validation class
# class ProductValidation:
#     @staticmethod
#     def validate(data, partial=False):
#         errors = {}
#         required_fields = ['name', 'description', 'category', 'price', 'brand', 'quantity']
        
#         if not partial:
#             for field in required_fields:
#                 if field not in data or data[field] is None or data[field] == '':
#                     errors[field] = f"{field} is required"
        
#         # check if all the fields are valid
#         if 'name' in data and data['name']:
#             if not isinstance(data['name'], str):
#                 errors['name'] = "Name should be a string"
        
#         if 'description' in data and data['description']:
#             if not isinstance(data['description'], str):
#                 errors['description'] = "Description should be a string"
        
#         if 'category' in data and data['category']:
#             if not isinstance(data['category'], str):
#                 errors['category'] = "Category should be a string"
        
#         if 'price' in data and data['price']:
#             try:
#                 price = float(data['price'])
#                 if price < 0:
#                     errors['price'] = "Price can't be negative"
#                 data['price'] = round(decimal.Decimal(price), 2)
#             except (ValueError, decimal.InvalidOperation):
#                 errors['price'] = "Price must be a valid number"
        
#         if 'brand' in data and data['brand']:
#             if not isinstance(data['brand'], str):
#                 errors['brand'] = "Brand should be a string"
        
        
#         if 'quantity' in data and data['quantity'] is not None:
#             try:
#                 quantity = int(data['quantity'])
#                 if quantity < 0:
#                     errors['quantity'] = "Quantity can't be negative"
#                 data['quantity'] = quantity
#             except ValueError:
#                 errors['quantity'] = "Quantity must be a valid integer"
        
#         return errors, data

# class ProductPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 10

# class ProductListCreateView(APIView):
#     def get(self, request):         #get products list with pagination
#         products = list(PRODUCTS.values())
        
#         paginator = ProductPagination()
#         paginated_products = paginator.paginate_queryset(products, request)
        
#         return paginator.get_paginated_response(paginated_products)
    
#     def post(self, request):        #create new product
#         global NEXT_ID
        
#         errors, validated_data = ProductValidation.validate(request.data)       #check for valid data
        
#         if errors:
#             return Response(
#                 {"error": "Validation failed", "details": errors}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")         #timestamp string for created_at and updated_at
        
#         product_data = {
#             'id': NEXT_ID,
#             **validated_data,
#             'created_at': now,
#             'updated_at': now
#         }
        
#         PRODUCTS[NEXT_ID] = product_data            #store in memory
#         NEXT_ID += 1
        
#         return Response(product_data, status=status.HTTP_201_CREATED)

# class ProductDetailView(APIView):
#     def get_product(self, product_id):              #fetch product by id
#         try:
#             product_id = int(product_id)
#             return PRODUCTS.get(product_id)
#         except (ValueError, TypeError):
#             return None
    
#     def get(self, request, product_id):
#         product = self.get_product(product_id)
        
#         if product:
#             return Response(product)
#         else:
#             return Response(
#                 {"error": f"Product not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
    
#     def put(self, request, product_id):         #update product on basis of id
#         product = self.get_product(product_id)
        
#         if not product:
#             return Response(
#                 {"error": f"Product not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         errors, validated_data = ProductValidation.validate(request.data)
        
#         if errors:
#             return Response(
#                 {"error": "Validation failed", "details": errors}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
#         updated_data = {
#             **product,
#             **validated_data,
#             'updated_at': now
#         }
        
#         PRODUCTS[product_id] = updated_data
        
#         return Response(updated_data)
    
#     def delete(self, request, product_id):      #delete a product on the basis of id
#         product = self.get_product(product_id)
        
#         if not product:
#             return Response(
#                 {"error": f"Product not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
    
#         del PRODUCTS[product_id]        #remove from memory
        
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(APIView):
    def __init__(self):
        self.product_service=ProductService()         #initialise ProductService instance
        super().__init__()
    
    #fetch products
    def get(self, request):
        created_aft = request.GET.get('created_after')      #fetch products on the basis of these parameters passed in api call
        updated_aft = request.GET.get('updated_after')

        products = self.product_service.get_all_products()

        if created_aft:                                       #finds prod. created after a given timestamp
            created_aft = datetime.fromisoformat(created_aft.replace("Z", "+00:00"))
            products = products.filter(created_at__gte=created_aft)

        if updated_aft:                                       #finds prod. updated after a given timestamp
            updated_aft = datetime.fromisoformat(updated_aft.replace("Z", "+00:00"))
            products = products.filter(updated_at__gte=updated_aft)
       
        ser = ProductSerializer(products, many=True)
        return Response(ser.data)
    
    #create product
    def post(self, request):
        ser = ProductSerializer(data=request.data)
        if ser.is_valid():
            product = self.product_service.create_product(ser.validated_data)
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def __init__(self):
        self.product_service = ProductService()
        super().__init__()
    
    #fetch product by id
    def get(self,request,prod_id):
        product = self.product_service.get_product_by_id(prod_id)
        if not product:
            return Response({"error": "product not found"},status=status.HTTP_404_NOT_FOUND)
        ser = ProductSerializer(product)
        return Response(ser.data)
    
    #update product by id if it exists
    def put(self, request, prod_id):
        ser = ProductSerializer(data=request.data)
        if ser.is_valid():
            product = self.product_service.update_product(prod_id, ser.validated_data)
            if not product:
                return Response({"error": "product not found"},status=status.HTTP_404_NOT_FOUND)
            return Response(ProductSerializer(product).data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #delete product by id if it exists
    def delete(self, request, prod_id):
        if self.product_service.delete_product(prod_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"product deleted successfully"},status=status.HTTP_404_NOT_FOUND)

#api view for products updated in last 2 days  
class RecentUpdatedProductsView(APIView):
    def __init__(self):
        self.product_service = ProductService()
        super().__init__()

    def get(self, request):
        two_days = datetime.now(timezone.utc) - timedelta(days=2)
        products = self.product_service.get_all_products()

        products = products.filter(updated_at__gte=two_days)

        ser = ProductSerializer(products, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

#api view for finding all the updates made in the product(tracking prod. history)  
class ProductHistoryView(APIView):
    def get(self, request, prod_id):
        hist = ProductHistory.objects(product_id=prod_id)
        ser= ProductHistorySerializer(hist, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)