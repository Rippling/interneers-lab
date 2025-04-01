from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from product.serializers.product_serializer import ProductSerializer
from product.services.product_service import ProductService

class ProductController(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        try:
            product = ProductService.create_product(request.data)
            print("Product created:", product, type(product))
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            print("Product created:", product, type(product))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, product_id=None):
        """Handle fetching products by category or product ID."""
        category_name = request.GET.get("category") 

        if product_id:
            product, error = ProductService.get_product_by_id(product_id)
            if error:
                return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

        if category_name:
            products, error = ProductService.get_filtered_products(category_name)
            if error:
                return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
            return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)
        products = ProductService.get_all_products()
        return Response(ProductSerializer(products, many=True).data)
        # return Response({"error": "Invalid request. Provide 'category' or 'product_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        """Update a product OR add/remove a category to it."""
        category_id = request.data.get("category_id") 
        action = request.data.get("action")  # Get action (add/remove) from request body

        if category_id and action:  
            if action == "add":
                product, error = ProductService.add_category_to_product(product_id, category_id)
                if error:
                    return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
                return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

            elif action == "remove":
                product, error = ProductService.remove_category_from_product(product_id, category_id)
                if error:
                    return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
                return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action. Use 'add' or 'remove'."}, status=status.HTTP_400_BAD_REQUEST)

        # Otherwise, update product details if no category-related action is provided
        updated_product = ProductService.update_product(product_id, request.data)
        if updated_product:
            return Response(ProductSerializer(updated_product).data, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
#synatx to add/remove a category from a product category list
# {
#   "category_id": "{category_id}",
#   "action": "add"
# }


    def delete(self, request, product_id):
        """Delete a product OR remove a category from it."""
        category_id = request.data.get("category_id")  

        if category_id:  # If category_id is provided, remove category
            product, error = ProductService.remove_category_from_product(product_id, category_id)
            if error:
                return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Category removed from product successfully"}, status=status.HTTP_200_OK)

        # Otherwise, delete the entire product
        success = ProductService.delete_product(product_id)
        if success:
            return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)