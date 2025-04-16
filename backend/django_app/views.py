from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import ProductService, ProductCategoryService


# -----------------------
# ProductCategory Views
# -----------------------
@csrf_exempt
def create_category(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = ProductCategoryService.create_category(data)
            return JsonResponse({"message": "Category created", "id": str(category.id)}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def get_category(request, category_id):
    category = ProductCategoryService.get_category(category_id)
    if not category:
        return JsonResponse({"error": "Category not found"}, status=404)
    return JsonResponse(category)

def list_categories(request):
    categories = ProductCategoryService.list_categories()
    return JsonResponse(categories, safe=False)

@csrf_exempt
def update_category(request, category_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_count = ProductCategoryService.update_category(category_id, data)
            if updated_count == 0:
                return JsonResponse({"error": "Category not found"}, status=404)
            return JsonResponse({"message": "Category updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_category(request, category_id):
    if request.method == 'DELETE':
        deleted_count = ProductCategoryService.delete_category(category_id)
        if deleted_count == 0:
            return JsonResponse({"error": "Category not found"}, status=404)
        return JsonResponse({"message": "Category deleted successfully"})


# -----------------------
# Product Views
# -----------------------
@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product = ProductService.create_product(data)
            return JsonResponse({"message": "Product created", "id": str(product['id'])}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

def get_product(request, product_id):
    product = ProductService.get_product(product_id)
    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)
    return JsonResponse(product)

def list_products(request):
    """List all products with optional field filters and ordering"""
    fields = request.GET.getlist("fields")  # Fields to include
    order_by = request.GET.get("order_by")  # Ordering field

    products = ProductService.list_products(fields=fields, order_by=order_by)
    return JsonResponse(products, safe=False)


def list_products_by_category(request, category_title):
    """List products belonging to a category with optional field filters and ordering"""
    fields = request.GET.getlist("fields")  # Fields to include
    order_by = request.GET.get("order_by")  # Ordering field

    products = ProductService.get_products_by_category(category_title, fields=fields, order_by=order_by)
    return JsonResponse(products, safe=False)

@csrf_exempt
def update_product(request, product_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_count = ProductService.update_product(product_id, data)
            if updated_count == 0:
                return JsonResponse({"error": "Product not found"}, status=404)
            return JsonResponse({"message": "Product updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        deleted_count = ProductService.delete_product(product_id)
        if deleted_count == 0:
            return JsonResponse({"error": "Product not found"}, status=404)
        return JsonResponse({"message": "Product deleted successfully"})
