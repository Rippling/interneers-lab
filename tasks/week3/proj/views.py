
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .repository import CategoryRepository, ProductRepository
from .service import CategoryService, ProductService

# week3

#note the diff bw this views.py and week2 views
#we used DRF directly to handle the api calls, it also directly interacted with the DB
#in CSR arch, we have to separate all of them. 
# we cant directly use DRF as it internally demands a query_set , but this query set is the directory layer's job. hence we cant use it as we separate it in CSR architecture.
# repo = ProductRepository()
# service = ProductService(repo)

# # ProductService class constructor needs an object of the ProductRepository class as parameter.

# class ProductAPI(APIView): #inherits from APIView class
#     def get(self, request):
#         products = service.get_all_products()
#         return Response(products, status=status.HTTP_200_OK)
 
#     def post(self, request):
#         try:
#             # Hand raw data to the service
#             new_id = service.create_product(request.data)
#             return Response({"message": "Success", "id": new_id}, status=status.HTTP_201_CREATED)
#         except ValueError as e:
#             # Catch the validation errors
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class ProductDetailAPI(APIView):
#     def delete(self, request, product_id):
#         success = service.delete_product(product_id)
#         if success:
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)



#week4
cat_repo = CategoryRepository()
cat_service = CategoryService(cat_repo)

prod_repo = ProductRepository()
prod_service = ProductService(prod_repo)

class CategoryAPI(APIView):
    def post(self, request):
        try:
            new_id = cat_service.create_category(request.data)
            return Response({"id": new_id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        categories = cat_service.get_all_categories()
        return Response(categories, status=status.HTTP_200_OK)

class CategoryProductsAPI(APIView):
    # Requirement 3: Fetch products for a category
    def get(self, request, category_id):
        products = prod_service.get_products_by_category(category_id)
        return Response(products, status=status.HTTP_200_OK)

class ProductCategoryUpdateAPI(APIView):
    # Requirement 4: Add/Remove products from categories
    def patch(self, request, product_id):
        # Send a category_id to add it, or None/null to remove it
        category_id = request.data.get('category_id')
        success = prod_service.update_product_category(product_id, category_id)
        
        if success:
            return Response({"message": "Updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class BulkProductUploadAPI(APIView):
    # Requirement 6: Bulk upload via CSV
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            count = prod_service.process_bulk_csv(file)
            return Response({"message": f"Successfully created {count} products"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            # If the service raises a ValueError (like a missing brand), return a 400 Bad Request
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CategoryDetailAPI(APIView):
    # Requirement 3: Delete a category
    def delete(self, request, category_id):
        success = cat_service.delete_category(category_id)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)