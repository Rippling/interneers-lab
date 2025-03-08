from rest_framework import serializers
from .models import Product  # Import the Product model

class ProductSerializer(serializers.ModelSerializer):  # Use ModelSerializer
    class Meta:
        model = Product
        fields = '__all__'  # Automatically includes all model fields

    def validate_name(self, value):
        """Ensure the product name is unique."""
        if Product.objects.filter(name=value).exists():
            raise serializers.ValidationError("A product with this name already exists.")
        return value

    def validate_price(self, value):
        """Ensure the price is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Price must be a non-negative value.")
        return value

    def validate_quantity(self, value):
        """Ensure the quantity is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Quantity must be a non-negative value.")
        return value
