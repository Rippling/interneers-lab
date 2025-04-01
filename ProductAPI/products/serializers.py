from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'uuid', 'sku', 'name', 'slug', 'description',
            'category', 'category_name', 'brand', 'tags',
            'price', 'discount_price', 'quantity', 'low_stock_threshold',
            'weight', 'dimensions', 'status', 'featured', 'rating',
            'is_in_stock', 'is_low_stock',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'slug', 'created_at', 'updated_at']

    def validate(self, data):
        # Validate discount price is less than regular price
        if 'discount_price' in data and data['discount_price']:
            if data['discount_price'] >= data.get('price', self.instance.price if self.instance else 0):
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
        # Custom SKU format validation (example: ABC-12345)
        import re
        if not re.match(r'^[A-Z]{3}-\d{5}$', value):
            raise serializers.ValidationError(
                'SKU must be in format: ABC-12345 (3 uppercase letters, hyphen, 5 digits)'
            )
        return value

    def validate_tags(self, value):
        # Validate tags format and clean them
        if value:
            tags = [tag.strip() for tag in value.split(',')]
            tags = [tag for tag in tags if tag]  # Remove empty tags
            return ','.join(tags)
        return value 