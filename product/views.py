from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer

products = []

class ProductAPI(APIView):
    def post(self, request):
        """Create a new product with validation."""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product_id = len(products) + 1  
            product_data = serializer.validated_data
            product_data["id"] = product_id
            products.append(product_data)
            return Response(
                {"message": "Product created successfully.", "product": product_data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, product_id=None):
        """Fetch a product by ID or list all products with pagination."""
        if product_id:
            product = next((p for p in products if p["id"] == product_id), None)
            if product:
                return Response(product)
            return Response(
                {"error": "Product not found", "details": f"No product found with ID {product_id}"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Pagination logic
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 5))
            if page <= 0 or limit <= 0:
                raise ValueError("Page and limit must be positive integers.")
        except ValueError:
            return Response(
                {"error": "Invalid pagination parameters", "details": "Both 'page' and 'limit' must be positive integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start = (page - 1) * limit
        end = start + limit
        paginated_products = products[start:end]

        return Response({
            "total_products": len(products),
            "page": page,
            "limit": limit,
            "total_pages": (len(products) + limit - 1) // limit,  
            "products": paginated_products
        })

    def put(self, request, product_id):
        """Update a product with validation."""
        for product in products:
            if product["id"] == product_id:
                serializer = ProductSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    product.update(serializer.validated_data)
                    return Response(
                        {"message": "Product updated successfully.", "product": product}
                    )
                return Response(
                    {"error": "Invalid data", "details": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": "Product not found", "details": f"No product found with ID {product_id}"},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, product_id):
        """Delete a product with validation."""
        global products
        if any(p["id"] == product_id for p in products):
            products = [p for p in products if p["id"] != product_id]
            return Response(
                {"message": "Product deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {"error": "Product not found", "details": f"No product found with ID {product_id}"},
            status=status.HTTP_404_NOT_FOUND
        )
