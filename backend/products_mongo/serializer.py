from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField()  # Assuming category is passed as an ID
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    brand = serializers.CharField(max_length=50, required=True)  # Explicit validation
    quantity_in_warehouse = serializers.IntegerField(required=False)

    def validate_brand(self, value):
        if not value.strip():  # Ensure it's not empty or just spaces
            raise serializers.ValidationError("Brand field is required.")
        return value

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
