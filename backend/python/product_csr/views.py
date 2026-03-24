import csv
import json
from io import StringIO

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from product_csr.repositories.category_repository import MongoCategoryRepository
from product_csr.repositories.product_repository import MongoProductRepository
from product_csr.services.category_service import CategoryService
from product_csr.services.product_service import ProductService


category_repo = MongoCategoryRepository()
product_repo = MongoProductRepository(category_repo=category_repo)

category_service = CategoryService(category_repo)
product_service = ProductService(product_repo, category_repo)


@csrf_exempt
def products(request):
    if request.method == "GET":
        filters = {
            "brand": request.GET.get("brand"),
            "search": request.GET.get("search"),
            "min_price": request.GET.get("min_price"),
            "max_price": request.GET.get("max_price"),
            "min_quantity": request.GET.get("min_quantity"),
            "max_quantity": request.GET.get("max_quantity"),
            "categories": request.GET.get("categories"),
        }

        return JsonResponse({"products": product_service.get_all_products(filters)})

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product = product_service.create_product(data)
            return JsonResponse(product, status=201)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def product_detail(request, product_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            result = product_service.update_product(product_id, data)
            return JsonResponse(result)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)

    if request.method == "DELETE":
        try:
            result = product_service.delete_product(product_id)
            return JsonResponse(result)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def categories(request):
    if request.method == "GET":
        return JsonResponse({"categories": category_service.get_all_categories()})

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            category = category_service.create_category(data)
            return JsonResponse(category, status=201)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def category_detail(request, category_id):
    if request.method == "GET":
        try:
            category = category_service.get_category(category_id)
            return JsonResponse(category)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=404)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            category = category_service.update_category(category_id, data)
            return JsonResponse(category)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)

    if request.method == "DELETE":
        try:
            result = category_service.delete_category(category_id)
            return JsonResponse(result)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=404)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def category_products(request, category_id):
    if request.method == "GET":
        try:
            products = product_service.get_products_by_category(category_id)
            return JsonResponse({"products": products})
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def add_product_to_category(request, category_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            result = product_service.add_product_to_category(product_id, category_id)
            return JsonResponse(result)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def remove_product_from_category(request, category_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            result = product_service.remove_product_from_category(product_id)
            return JsonResponse(result)
        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def bulk_upload_product(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("file")
            if not file:
                return JsonResponse({"error": "CSV file is required"}, status=400)

            data = file.read().decode("utf-8")
            csv_file = StringIO(data)
            reader = csv.DictReader(csv_file)

            if not reader.fieldnames:
                return JsonResponse({"error": "Empty CSV file"}, status=400)

            required_fields = ["name", "price", "quantity", "brand"]
            for field in required_fields:
                if field not in reader.fieldnames:
                    return JsonResponse({"error": f"Missing column: {field}"}, status=400)

            products = []
            skipped = 0

            for row in reader:
                if not row.get("brand"):
                    skipped += 1
                    continue

                try:
                    row["price"] = float(row["price"])
                    row["quantity"] = int(row["quantity"])
                except ValueError:
                    skipped += 1
                    continue

                product = product_service.create_product(row)
                products.append(product)

            return JsonResponse({
                "message": "Bulk upload successful",
                "uploaded": len(products),
                "skipped": skipped,
                "data": products,
            })
        except Exception:
            return JsonResponse({"error": "Something went wrong"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)
