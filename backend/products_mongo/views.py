from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .product_service import ProductService
from .product_repository import ProductRepository

@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product = ProductService.create_product(data)
            return JsonResponse({
            "message": "Product created!",
            "product": ProductRepository.format_product(product)  # ✅ Now it's safe to format here
        }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, product_id=None):
        """Retrieve a single product or all products with pagination."""
        if product_id:
            product = ProductService.get_product_by_id(product_id)
            if product:
                return JsonResponse({"product": product}, status=200)
            return JsonResponse({"error": "Product not found"}, status=404)

        try:
            page = int(request.GET.get("page", 1))
            per_page = int(request.GET.get("per_page", 10))
            products = ProductService.get_all_products(page, per_page)
            return JsonResponse({"products": products}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, product_id):
        """Update a product by ID."""
        try:
            data = json.loads(request.body)
            updated_product = ProductService.update_product(product_id, data)
            if updated_product:
                return JsonResponse({"message": "Product updated!", "product": updated_product}, status=200)
            return JsonResponse({"error": "Product not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, product_id):
        """Delete a product by ID."""
        deleted = ProductService.delete_product(product_id)
        if deleted:
            return JsonResponse({"message": "Product deleted!"}, status=200)
        return JsonResponse({"error": "Product not found"}, status=404)