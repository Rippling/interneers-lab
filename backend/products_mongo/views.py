from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .product_service import ProductService
from .product_repository import ProductRepository
from .product_category_services import ProductCategoryService
from .product_category_repository import ProductCategoryRepository

@method_decorator(csrf_exempt, name='dispatch')
class ProductView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            product = ProductService.create_product(data)
            return JsonResponse({
                "message": "Product created!",
                "product": ProductRepository.format_product(product)
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, product_id=None):
        """Retrieve a single product or filter products with advanced search options."""
        if product_id:
            product = ProductService.get_by_id(product_id)
            if product:
                return JsonResponse({"product": ProductRepository.format_product(product)}, status=200)
            return JsonResponse({"error": "Product not found"}, status=404)

        try:
            # ✅ Extract filter parameters from the request
            category_id = request.GET.get("category_id")
            name = request.GET.get("name")
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            brand = request.GET.get("brand")
            page = int(request.GET.get("page", 1))
            per_page = int(request.GET.get("per_page", 10))

            # ✅ Fetch products based on the filters
            products = ProductService.get_filtered_products(
                category_id=category_id,
                name=name,
                min_price=min_price,
                max_price=max_price,
                brand=brand,
                page=page,
                per_page=per_page
            )

            formatted_products = [ProductRepository.format_product(prod) for prod in products]
            return JsonResponse({"products": formatted_products}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, product_id, category_id=None):
        """Update a product OR assign a product to a category."""
        try:
            if category_id:
                updated_product = ProductService.add_product_to_category(product_id, category_id)
                if updated_product:
                    return JsonResponse({
                        "message": "Product assigned to category!",
                        "product": ProductRepository.format_product(updated_product)
                    }, status=200)
                return JsonResponse({"error": "Product or Category not found"}, status=404)

            data = json.loads(request.body)
            updated_product = ProductService.update_product(product_id, data)
            if updated_product:
                return JsonResponse({"message": "Product updated!", "product": updated_product}, status=200)
            return JsonResponse({"error": "Product not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, product_id, category_id=None):
        """Delete a product OR remove a product from its category."""
        try:
            if category_id:
                updated_product = ProductService.remove_product_from_category(product_id)
                if updated_product:
                    return JsonResponse({
                        "message": "Product removed from category!",
                        "product": ProductRepository.format_product(updated_product)
                    }, status=200)
                return JsonResponse({"error": "Product not found"}, status=404)

            deleted = ProductService.delete_product(product_id)
            if deleted:
                return JsonResponse({"message": "Product deleted!"}, status=200)
            return JsonResponse({"error": "Product not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ProductCategoryView(View):
    def post(self, request):
        """Create a new product category."""
        try:
            data = json.loads(request.body)
            category = ProductCategoryService.create_category(data)
            return JsonResponse({
                "message": "Category created!",
                "category": ProductCategoryRepository.format_category(category)
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request, category_id=None):
        """Retrieve a single category or all categories."""
        if category_id:
            category = ProductCategoryService.get_category_by_id(category_id)
            if category:
                return JsonResponse({"category": ProductCategoryRepository.format_category(category)}, status=200)
            return JsonResponse({"error": "Category not found"}, status=404)

        try:
            categories = ProductCategoryService.get_all_categories()
            formatted_categories = [ProductCategoryRepository.format_category(cat) for cat in categories]
            return JsonResponse({"categories": formatted_categories}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def put(self, request, category_id):
        """Update a product category."""
        try:
            data = json.loads(request.body)
            updated_category = ProductCategoryService.update_category(category_id, data)
            if updated_category:
                return JsonResponse({
                    "message": "Category updated!",
                    "category": ProductCategoryRepository.format_category(updated_category)
                }, status=200)
            return JsonResponse({"error": "Category not found"}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, category_id):
        """Delete a category."""
        deleted = ProductCategoryService.delete_category(category_id)
        if deleted:
            return JsonResponse({"message": "Category deleted!"}, status=200)
        return JsonResponse({"error": "Category not found"}, status=404)
