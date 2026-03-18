from rest_framework import serializers
from .repositories import ProductRepository, ProductCategoryRepository

class ProductSerializer(serializers.Serializer):

    product_repository = ProductRepository()
    
    name = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(required=True, max_length=500)
    brand = serializers.CharField(required=True, max_length=200)
    price = serializers.DecimalField(min_value=0, max_digits=8, decimal_places=2)
    quantity = serializers.IntegerField(min_value=0)
    product_category = serializers.CharField()
    created_at = serializers.DateTimeField(read_only = True)
    updated_at = serializers.DateTimeField(read_only = True)

    def create(self, validated_data):
        return self.product_repository.add(validated_data)
    
    def update(self, instance, validated_data):
        return self.product_repository.update(instance, validated_data)


class ProductCategorySerializer(serializers.Serializer):

    product_category_repository = ProductCategoryRepository()

    title = serializers.CharField(required=True, max_length=200)
    description = serializers.CharField(max_length=400)

    def create(self, validated_data):
        return self.product_category_repository.add(validated_data)
    
    def update(self, instance, validated_data):
        return self.product_category_repository.update(instance, validated_data)

