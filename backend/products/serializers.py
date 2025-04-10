from rest_framework import serializers
from rest_framework_dataclasses.serializers import DataclassSerializer
from products.repositories.product_category_repository import ProductCategoryDetail
from products.repositories.product_repository import ProductDetail

class ProductCategoryDetailSerializer(DataclassSerializer):
    class Meta:
        dataclass = ProductCategoryDetail

        extra_kwargs = {
            "id": {"read_only": True, "required": False},
            "description": {"required": False},
            "title": {"max_length": 200},
        }

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters.")
        return value


class ProductDetailSerializer(DataclassSerializer):
    class Meta:
        dataclass = ProductDetail
        extra_kwargs = {
            "id": {"read_only": True, "required": False},
            "description": {"required": False},
            "category": {"required": True},
            "price": {"required": True},
            "brand": {"max_length": 50},
        }