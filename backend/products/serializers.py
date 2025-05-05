from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField(allow_blank=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)
    sku = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField(allow_blank=True, required=False)
    category = serializers.CharField()  # Pass category id/slug
    category_name = serializers.CharField(read_only=True)
    brand = serializers.CharField(max_length=100, required=False, allow_blank=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    quantity = serializers.IntegerField()
    low_stock_threshold = serializers.IntegerField(required=False)
    weight = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    dimensions = serializers.CharField(max_length=50, required=False, allow_blank=True)
    status = serializers.CharField(max_length=20, required=False)
    featured = serializers.BooleanField(required=False)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, allow_null=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        # Validate discount price is less than regular price
        if 'discount_price' in data and data['discount_price']:
            if data['discount_price'] >= data.get('price', 0):
                raise serializers.ValidationError({
                    'discount_price': 'Discount price must be less than regular price'
                })
        # Validate dimensions format if provided
        if 'dimensions' in data and data['dimensions']:
            try:
                l, w, h = data['dimensions'].split('x')
                float(l), float(w), float(h)
            except (ValueError, TypeError):
                raise serializers.ValidationError({
                    'dimensions': 'Dimensions must be in format: length x width x height (e.g., "10x20x30")'
                })
        return data

    def validate_sku(self, value):
        import re
        if not re.match(r'^[A-Z]{3}-\d{5}$', value):
            raise serializers.ValidationError(
                'SKU must be in format: ABC-12345 (3 uppercase letters, hyphen, 5 digits)'
            )
        return value

    def validate_tags(self, value):
        # Validate tags format and clean them
        if value:
            tags = [tag.strip() for tag in value if tag]
            return tags
        return value 