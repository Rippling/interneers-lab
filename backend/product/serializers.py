from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  # MongoDB uses string ObjectId
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)
    category = serializers.CharField(max_length=255)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        return Product(**validated_data).save()

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")
        return value
    
    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product description cannot be empty.")
        return value
    
    def validate_category(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product category cannot be empty.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be greater than or equal to zero.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be greater than or equal to zero.")
        return value
