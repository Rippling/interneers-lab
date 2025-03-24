from rest_framework import serializers
from .models.ProductModel import Product
from .models.CategoryModel import ProductCategory

class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data):
        return ProductCategory(**validated_data).save()
    
 

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    brand = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField()  # Storing category as an ObjectId (string)
    price = serializers.FloatField()
    quantity = serializers.IntegerField()

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Product name cannot be empty.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

    def create(self, validated_data):
        """Manually create a Product instance for MongoEngine"""
        category_id = validated_data.pop("category", None)
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            raise serializers.ValidationError("Invalid category ID.")
        
        product = Product(category=category, **validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):
        """Manually update a Product instance"""
        for key, value in validated_data.items():
            if key == "category":
                category = ProductCategory.objects(id=value).first()
                if not category:
                    raise serializers.ValidationError("Invalid category ID.")
                instance.category = category
            else:
                setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Convert MongoEngine object to a serializable format"""
        data = {
            "id": str(instance.id),
            "name": instance.name,
            "description": instance.description,
            "brand": instance.brand,
            "category": instance.category.title if instance.category else None,
            "price": float(instance.price),
            "quantity": int(instance.quantity),
        }
        return data
