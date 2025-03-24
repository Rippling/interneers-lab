from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.CategoryModel import ProductCategory
from ..serializers import ProductCategorySerializer
from ..serializers import ProductSerializer
from ..services.CategoryService import CategoryService

class CategoryView(APIView):
    def post(self, request):
        print("Received Data:", request.data)  
   
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            print("Saved Data:", category.to_mongo().to_dict())
            return Response({"message": "Category created successfully", "category": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, title):
        products, error = CategoryService.get_products_by_category_title(title)

        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, title):
        category = ProductCategory.objects(title=title).first()
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductCategorySerializer(category, data=request.data, partial=True)
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
