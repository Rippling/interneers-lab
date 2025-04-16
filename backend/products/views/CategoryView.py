from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import NotFound
from ..models.CategoryModel import ProductCategory
from ..serializers import ProductCategorySerializer
from ..serializers import ProductSerializer
from ..services.CategoryService import CategoryService
from rest_framework.pagination import PageNumberPagination
from bson import ObjectId
from rest_framework.exceptions import ValidationError
from mongoengine.errors import DoesNotExist , NotUniqueError

class CategoryPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryView(APIView):
    def post(self, request):
        print("Received Data:", request.data)  
        try:
            serializer = ProductCategorySerializer(data=request.data)
            if serializer.is_valid():
                category = serializer.save()
                print("Saved Data:", category.to_mongo().to_dict())
                return Response({"message": "Category created successfully", "category": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NotUniqueError:
            return Response({'error': 'Category with this title already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, title):
        products, error = CategoryService.get_products_by_category_title(title)

        if error:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, title):
        print("PUT method reached")
        category = ProductCategory.objects(title=title).first()
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductCategorySerializer(instance=category, data=request.data)
        
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response({"message": "Category updated successfully", "category": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, title):
        category = ProductCategory.objects(title=title).first()
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_200_OK)

class CategoryDetail(generics.RetrieveAPIView):
        serializer_class = ProductCategorySerializer
        lookup_field = "id"

        def get_object(self):
            category_id = self.kwargs.get("id")

            if not ObjectId.is_valid(category_id):
                raise ValidationError({"error": "Invalid ID format"})
        
            try:
                category = ProductCategory.objects.get(id=category_id)
            except DoesNotExist:
                raise NotFound("Category not found")
            category = CategoryService.getCategoryById(category_id)
            print("dfdf" , category)
            if not category:
                raise NotFound("Category  not found") 
            return category
        
class CategoryList(generics.ListAPIView):
    serializer_class = ProductCategorySerializer
    pagination_class = CategoryPagination

    def get_queryset(self):
        queryset = CategoryService.get_all_categories()
        print(f"Queryset: {queryset}") 
        if queryset is None:
            return ProductCategory.objects.none() 
        return queryset
