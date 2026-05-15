from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProductCategoryActionSerializer, ProductCategorySerializer, ProductSerializer
from .service import product_category_service, product_service
from .repository import product_category_repository
from .pagination import Week4Pagination


class ProductListCreateAPIView(APIView):
    # listing all products with sorting, filtering and pagination
    def get(self, request):
        sort_by = request.query_params.get("sort_by", "id")

        filters = {}

        name = request.query_params.get("name")
        brand = request.query_params.get("brand")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        min_quantity = request.query_params.get("min_quantity")
        max_quantity = request.query_params.get("max_quantity")
        category_id = request.query_params.get("category_id")

        if name:
            filters["name"] = name
        if brand:
            filters["brand"] = brand

        if min_price is not None:
            try:
                filters["min_price"] = float(min_price)
            except ValueError:
                return Response({"error": "min_price must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        if max_price is not None:
            try:
                filters["max_price"] = float(max_price)
            except ValueError:
                return Response({"error": "max_price must be a number"}, status=status.HTTP_400_BAD_REQUEST)

        if min_quantity is not None:
            try:
                filters["min_quantity"] = int(min_quantity)
            except ValueError:
                return Response({"error": "min_quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if max_quantity is not None:
            try:
                filters["max_quantity"] = int(max_quantity)
            except ValueError:
                return Response({"error": "max_quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if category_id is not None:
            try:
                category_id = int(category_id)
            except ValueError:
                return Response({"error": "category_id must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

            category = product_category_repository.get(category_id)
            if not category:
                return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

            filters["category"] = category

        products = product_service.list_all(filters=filters, sort_by=sort_by)
        paginator = Week4Pagination()
        paginated_products = paginator.paginate_queryset(
            products, request, view=self)

        product_data = []
        for product in paginated_products:
            product_data.append(product.to_dict())

        serializer = ProductSerializer(product_data, many=True)
        return paginator.get_paginated_response(serializer.data)

    # create one product
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = product_service.create(serializer.validated_data)
            # we have to use isinstance bcz service now returns error instead of true/false like in week2/3
            if isinstance(product, dict) and "error" in product:
                return Response(product, status=status.HTTP_400_BAD_REQUEST)
            response_serializer = ProductSerializer(product.to_dict())
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    # get product with id
    def get(self, request, id):
        product = product_service.get(id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product.to_dict())
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update product
    def put(self, request, id):
        existing_product = product_service.get(id)
        if not existing_product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            updated_product = product_service.update(
                id, serializer.validated_data)

            if isinstance(updated_product, dict) and "error" in updated_product:
                return Response(updated_product, status=status.HTTP_400_BAD_REQUEST)

            response_serializer = ProductSerializer(updated_product.to_dict())
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete product
    def delete(self, request, id):
        deleted = product_service.delete(id)
        if not deleted:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ProductCategoryListCreateAPIView(APIView):
    # list all category with pagination, sorting and filtering
    def get(self, request):
        sort_by = request.query_params.get("sort_by", "id")
        filters = {}
        title = request.query_params.get("title")

        if title:
            filters["title"] = title

        categories = product_category_service.list_all(
            filters=filters, sort_by=sort_by)

        paginator = Week4Pagination()
        paginated_categories = paginator.paginate_queryset(
            categories, request, view=self)

        category_data = []
        for category in paginated_categories:
            category_data.append(category.to_dict())

        serializer = ProductCategorySerializer(category_data, many=True)
        return paginator.get_paginated_response(serializer.data)

    # create one category
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = product_category_service.create(
                serializer.validated_data)
            if isinstance(category, dict) and "error" in category:
                return Response(category, status=status.HTTP_400_BAD_REQUEST)

            response_serializer = ProductCategorySerializer(category.to_dict())
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryDetailAPIView(APIView):
    # get one category
    def get(self, request, id):
        category = product_category_service.get(id)
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ProductCategorySerializer(category.to_dict())
            return Response(serializer.data, status=status.HTTP_200_OK)

    # update category
    def put(self, request, id):
        existing_category = product_category_service.get(id)
        if not existing_category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            updated_category = product_category_service.update(
                id, serializer.validated_data)
            if isinstance(updated_category, dict) and "error" in updated_category:
                return Response(updated_category, status=status.HTTP_400_BAD_REQUEST)

            response_serializer = ProductCategorySerializer(
                updated_category.to_dict())
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete category

    def delete(self, request, id):
        deleted = product_category_service.delete(id)
        if isinstance(deleted, dict) and "error" in deleted:
            if "Category not found" in deleted["error"]:
                return Response(deleted, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(deleted, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


# list all products of one category with filter + sort + paginate
class CategoryProductsAPIView(APIView):
    def get(self, request, category_id):
        sort_by = request.query_params.get("sort_by", "id")

        filters = {}

        name = request.query_params.get("name")
        brand = request.query_params.get("brand")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        min_quantity = request.query_params.get("min_quantity")
        max_quantity = request.query_params.get("max_quantity")

        if name:
            filters["name"] = name

        if brand:
            filters["brand"] = brand

        if min_price is not None:
            try:
                filters["min_price"] = float(min_price)
            except ValueError:
                return Response({"error": "min_price must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        if max_price is not None:
            try:
                filters["max_price"] = float(max_price)
            except ValueError:
                return Response({"error": "max_price must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        if min_quantity is not None:
            try:
                filters["min_quantity"] = int(min_quantity)
            except ValueError:
                return Response({"error": "min_quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if max_quantity is not None:
            try:
                filters["max_quantity"] = int(max_quantity)
            except ValueError:
                return Response({"error": "max_quantity must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        products = product_category_service.get_products(
            category_id,
            filters=filters,
            sort_by=sort_by,
        )

        if isinstance(products, dict) and "error" in products:
            return Response(products, status=status.HTTP_404_NOT_FOUND)

        paginator = Week4Pagination()
        paginated_products = paginator.paginate_queryset(
            products, request, view=self)

        product_data = []
        for product in paginated_products:
            product_data.append(product.to_dict())

        serializer = ProductSerializer(product_data, many=True)
        return paginator.get_paginated_response(serializer.data)


# add product to a category
class AddProductToCategoryAPIView(APIView):
    def post(self, request, category_id):
        serializer = ProductCategoryActionSerializer(data=request.data)

        if serializer.is_valid():
            product = product_category_service.add_product_to_category(
                category_id, serializer.validated_data["product_id"])
            if isinstance(product, dict) and "error" in product:
                if product["error"] in ["Category not found", "Product not found"]:
                    return Response(product, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(product, status=status.HTTP_400_BAD_REQUEST)
            response_serializer = ProductSerializer(product.to_dict())
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# remove product from category
class RemoveProductFromCategoryAPIView(APIView):
    def post(self, request, category_id):
        serializer = ProductCategoryActionSerializer(data=request.data)

        if serializer.is_valid():
            product = product_category_service.remove_product_category(
                category_id, serializer.validated_data["product_id"])

            if isinstance(product, dict) and "error" in product:
                if product["error"] in ["Category not found", "Product not found"]:
                    return Response(product, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response(product, status=status.HTTP_400_BAD_REQUEST)

            response_serializer = ProductSerializer(product.to_dict())
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# upload csv and create many products
class BulkProductUploadAPIView(APIView):
    # normally DRF expects JSON bodies but it is not coming in form of JSON so we need to parse it
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # get uploaded file first
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return Response({"error": "CSV file is required with key 'file'"}, status=status.HTTP_400_BAD_REQUEST)

        # send file to service layer
        result = product_service.create_from_csv(uploaded_file)

        if isinstance(result, dict) and "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        # if service did not return error prepare dict to upload
        product_data = []
        for product in result:
            product_data.append(product.to_dict())

        serializer = ProductSerializer(product_data, many=True)
        return Response({
            "message": f"{len(product_data)} products created successfully.",
            "products": serializer.data
        }, status=status.HTTP_201_CREATED)
