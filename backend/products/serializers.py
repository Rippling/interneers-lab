from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Product, ProductCategory


class ProductSerializer(DocumentSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate_brand(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Brand is required.")
        return value


class ProductCategorySerializer(DocumentSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"
