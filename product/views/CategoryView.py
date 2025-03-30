from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.CategoryService import CategoryService
from ..serializers import ProductCategorySerializer,ProductSerializer

#api view for listing and creation prod. categories
class ProdCategoryListView(APIView):
    def __init__(self):
        self.category_service=CategoryService()
        super().__init__()

    #fetch all categories
    def get(self, request):
        categories=self.category_service.get_all_categories()
        ser=ProductCategorySerializer(categories, many=True)
        return Response(ser.data)

    #create new category
    def post(self, request):
        ser=ProductCategorySerializer(data=request.data)
        if ser.is_valid():
            category=self.category_service.create_category(ser.validated_data)
            return Response(ProductCategorySerializer(category).data,status=status.HTTP_201_CREATED)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

#api view for fetching,updating and deleting specific category
class ProdCategoryDetailView(APIView):
    def __init__(self):
        self.category_service=CategoryService()
        super().__init__()

    #search category by id or title
    def get(self, request, category_id=None, title=None):
        if category_id:
            category=self.category_service.get_category_by_id(category_id)
            if not category:
                return Response({"error": "Category not found"},status=status.HTTP_404_NOT_FOUND)
            ser=ProductCategorySerializer(category)
            return Response(ser.data)

        if title:
            categories=self.category_service.search_categories_by_title(title)
            ser=ProductCategorySerializer(categories, many=True)
            return Response(ser.data,status=status.HTTP_200_OK)

        return Response({"error": "Provide either category_id or title"}, status=status.HTTP_400_BAD_REQUEST)

    #update category on basis of id
    def put(self, request, category_id):
        ser=ProductCategorySerializer(data=request.data)
        if ser.is_valid():
            category=self.category_service.update_category(category_id, ser.validated_data)
            if not category:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(ProductCategorySerializer(category).data)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

    #remove category by id
    def delete(self, request, category_id):
        if self.category_service.delete_category(category_id):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

#api view for fetching prod. within a category
class CategoryProductsView(APIView):
    def __init__(self):
        self.category_service=CategoryService()
        super().__init__()

    def get(self, request, category_id):
        products=self.category_service.get_products_in_category(category_id)
        ser=ProductSerializer(products, many=True)
        return Response(ser.data)
    
#api view for adding and removing prod. from categories
class ProdCategoryManagementView(APIView):
    def __init__(self):
        self.category_service=CategoryService()
        super().__init__()

    #add prod. to a category
    def post(self, request):
        category_id=request.data.get('category_id')
        product_id=request.data.get('product_id')

        if not category_id or not product_id:
            return Response({
                "error": "Both category_id and product_id are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        result=self.category_service.add_prod_to_category(category_id, product_id)
        
        if result:
            return Response({
                "message": "Product added to category successfully."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Failed to add product to category."
            }, status=status.HTTP_404_NOT_FOUND)

    #remove prod. from its category
    def delete(self, request):
        product_id=request.data.get('product_id')
        
        if not product_id:
            return Response({
                "error": "product_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        result=self.category_service.remove_prod_from_category(product_id)
        
        if result:
            return Response({
                "message": "Product removed from category successfully."
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Failed to remove product from category."
            }, status=status.HTTP_404_NOT_FOUND)
        
    #explicitly handling get request to prevent method not allowed err
    def get(self, request):
        return Response({
                "error": "GET method not supported.Use POST to add a product to a category or DELETE to remove a product from a category."
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)