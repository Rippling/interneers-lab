import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..services.services import ProductService, ProductCategoryService

PAGE_SIZE = 10

# Shared service instances — safe since services hold no request-specific state.
# In tests, instantiate views directly with injected mock services.
product_service = ProductService()
category_service = ProductCategoryService()


def parse_json_body(request):
    """
    Parses the request body as JSON.
    Returns (data, None) on success or (None, JsonResponse error) on failure.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return None, JsonResponse(
            {"error": "Invalid JSON", "message": "Request body must be valid JSON."},
            status=400,
        )
    if not isinstance(data, dict):
        return None, JsonResponse(
            {
                "error": "Invalid request body",
                "message": "Request body must be a JSON object.",
            },
            status=400,
        )
    return data, None


def parse_pagination(request):
    """
    Parses page and page_size query params.
    Returns (page, page_size, None) on success or (None, None, JsonResponse) on failure.
    """
    try:
        page = int(request.GET.get("page", 1))
        if page < 1:
            raise ValueError
    except ValueError:
        return (
            None,
            None,
            JsonResponse(
                {
                    "error": "Invalid page number",
                    "message": "page must be a positive integer e.g. ?page=1",
                },
                status=400,
            ),
        )
    try:
        page_size = int(request.GET.get("page_size", PAGE_SIZE))
        if page_size < 1:
            raise ValueError
    except ValueError:
        return (
            None,
            None,
            JsonResponse(
                {
                    "error": "Invalid page_size",
                    "message": "page_size must be a positive integer e.g. ?page_size=5",
                },
                status=400,
            ),
        )
    return page, page_size, None


@method_decorator(csrf_exempt, name="dispatch")
class ProductCategoryListView(View):
    """
    GET  /categories/       — list all categories (paginated)
    POST /categories/       — create a new category
    """

    def get(self, request):
        page, page_size, err = parse_pagination(request)
        if err:
            return err

        result = category_service.get_all_categories(page, page_size)
        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=400)
        return JsonResponse(result, status=200)

    def post(self, request):
        data, err = parse_json_body(request)
        if err:
            return err

        result = category_service.create_category(data)
        if "error" in result:
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=400,
            )
        return JsonResponse(
            {
                "message": "Category created successfully",
                "category": result["category"],
            },
            status=201,
        )


@method_decorator(csrf_exempt, name="dispatch")
class ProductCategoryDetailView(View):
    """
    GET    /categories/<id>/          — fetch one category
    PUT    /categories/<id>/          — full update
    PATCH  /categories/<id>/          — partial update
    DELETE /categories/<id>/          — delete (blocked if products exist)
    GET    /categories/<id>/products/ — list all products in this category
    """

    http_method_names = ["get", "put", "patch", "delete"]

    def get(self, request, category_id):
        result = category_service.get_category(str(category_id))
        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=404)
        return JsonResponse(result["category"], status=200)

    def put(self, request, category_id):
        data, err = parse_json_body(request)
        if err:
            return err

        result = category_service.full_update_category(str(category_id), data)
        if "error" in result:
            status = 404 if result["error"] == "Category not found" else 400
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=status,
            )
        return JsonResponse(
            {
                "message": "Category updated successfully",
                "category": result["category"],
            },
            status=200,
        )

    def patch(self, request, category_id):
        data, err = parse_json_body(request)
        if err:
            return err

        result = category_service.partial_update_category(str(category_id), data)
        if "error" in result:
            status = 404 if result["error"] == "Category not found" else 400
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=status,
            )
        return JsonResponse(
            {
                "message": "Category partially updated successfully",
                "category": result["category"],
            },
            status=200,
        )

    def delete(self, request, category_id):
        result = category_service.delete_category(str(category_id))
        if "error" in result:
            # 409 Conflict when products exist, 404 when category not found
            status = 409 if "assigned to it" in result["error"] else 404
            return JsonResponse({"error": result["error"]}, status=status)
        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name="dispatch")
class ProductsByCategoryView(View):
    """
    GET /categories/<id>/products/  — list all products in a category
    """

    http_method_names = ["get"]

    def get(self, request, category_id):
        result = category_service.get_products_in_category(str(category_id))
        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=404)
        return JsonResponse(result, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class ProductListView(View):
    """
    GET  /products/      — list all products (paginated)
    POST /products/      — create a new product (optionally with category_id)
    POST /products/bulk/ — bulk create from CSV upload
    """

    def get(self, request):
        page, page_size, err = parse_pagination(request)
        if err:
            return err

        filter_params = {
            "category_ids": request.GET.get("category_ids", ""),
            "min_price": request.GET.get("min_price", ""),
            "max_price": request.GET.get("max_price", ""),
            "min_quantity": request.GET.get("min_quantity", ""),
            "max_quantity": request.GET.get("max_quantity", ""),
            "brand": request.GET.get("brand", ""),
            "search": request.GET.get("search", ""),
        }
        result = product_service.get_all_products(page, page_size, filter_params=filter_params)
        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=400)
        return JsonResponse(result, status=200)

    def post(self, request):
        data, err = parse_json_body(request)
        if err:
            return err

        result = product_service.create_product(data)
        if "error" in result:
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=400,
            )
        return JsonResponse(
            {"message": "Product created successfully", "product": result["product"]},
            status=201,
        )


@method_decorator(csrf_exempt, name="dispatch")
class ProductBulkView(View):
    """
    POST /products/bulk/

    Accepts a CSV file upload (multipart/form-data) with field name 'file',
    OR raw CSV text in the request body with Content-Type: text/csv.

    Expected CSV columns: name, description, price, brand, quantity, category_id (optional)

    All rows are validated before any are inserted. If any row fails,
    the entire import is rejected with per-row error details.
    """

    http_method_names = ["post"]

    def post(self, request):
        if request.FILES.get("file"):
            csv_file = request.FILES["file"]
            try:
                csv_content = csv_file.read().decode("utf-8")
            except UnicodeDecodeError:
                return JsonResponse(
                    {"error": "File encoding error", "message": "CSV file must be UTF-8 encoded."},
                    status=400,
                )
        else:
            return JsonResponse(
                {"error": "No CSV file provided",
                "message": "Upload a CSV file as multipart form field named 'file'."},
                status=400,
            )

        result = product_service.bulk_create_from_csv(csv_content)
        if "error" in result:
            return JsonResponse(result, status=400)
        return JsonResponse(result, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class ProductDetailView(View):
    """
    GET    /products/<id>/           — fetch one product
    PUT    /products/<id>/           — full update
    PATCH  /products/<id>/           — partial update
    DELETE /products/<id>/           — delete
    """

    http_method_names = ["get", "put", "patch", "delete"]

    def get(self, request, product_id):
        result = product_service.get_product(str(product_id))
        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=404)
        return JsonResponse(result["product"], status=200)

    def put(self, request, product_id):
        data, err = parse_json_body(request)
        if err:
            return err

        result = product_service.full_update_product(str(product_id), data)
        if "error" in result:
            status = 404 if result["error"] == "Product not found" else 400
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=status,
            )
        return JsonResponse(
            {
                "message": "Product fully updated successfully",
                "product": result["product"],
            },
            status=200,
        )

    def patch(self, request, product_id):
        data, err = parse_json_body(request)
        if err:
            return err

        result = product_service.partial_update_product(str(product_id), data)
        if "error" in result:
            status = 404 if result["error"] == "Product not found" else 400
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=status,
            )
        return JsonResponse(
            {
                "message": "Product partially updated successfully",
                "product": result["product"],
            },
            status=200,
        )

    def delete(self, request, product_id):
        result = product_service.delete_product(str(product_id))
        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=404)
        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name="dispatch")
class ProductCategoryMembershipView(View):
    """
    PUT    /products/<id>/category/  — assign product to a category
    DELETE /products/<id>/category/  — remove product from its category

    These are dedicated endpoints for the category membership relationship,
    keeping them separate from the general product update endpoints makes
    the intent explicit and keeps update() logic focused on data fields only.
    """

    http_method_names = ["put", "delete"]

    def put(self, request, product_id):
        """Assign product to a category. Body: {"category_id": "<id>"}"""
        data, err = parse_json_body(request)
        if err:
            return err

        category_id = data.get("category_id")
        if not category_id:
            return JsonResponse(
                {"error": "category_id is required in the request body"},
                status=400,
            )

        result = product_service.add_product_to_category(
            str(product_id), str(category_id)
        )
        if "error" in result:
            status = 404 if "not found" in result["error"] else 400
            return JsonResponse({"error": result["error"]}, status=status)
        return JsonResponse(
            {
                "message": "Product assigned to category successfully",
                "product": result["product"],
            },
            status=200,
        )

    def delete(self, request, product_id):
        """Remove product from its current category."""
        result = product_service.remove_product_from_category(str(product_id))
        if "error" in result:
            status = 404 if "not found" in result["error"] else 400
            return JsonResponse({"error": result["error"]}, status=status)
        return JsonResponse(
            {
                "message": "Product removed from category successfully",
                "product": result["product"],
            },
            status=200,
        )
