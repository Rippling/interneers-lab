from rest_framework import serializers
from .models.ProductModel import Product
from .models.CategoryModel import ProductCategory
from bson import ObjectId

class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data):
        return ProductCategory(**validated_data).save()
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
 

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    brand = serializers.CharField(required=False, allow_blank=True)
    category = serializers.ListField(child=serializers.CharField())
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

    def validate_category(self, value):

        if not isinstance(value, list):
            raise serializers.ValidationError("Category must be a list of valid category IDs.")
        
        categories = ProductCategory.objects(title__in=value)
        if len(categories) != len(value):
            raise serializers.ValidationError("Some categories are invalid.")
        
        return categories
    
    def create(self, validated_data):
        
        categories = validated_data.pop("category", [])
        product = Product(category=categories, **validated_data)
        product.save()
        return product

    def update(self, instance, validated_data):
    
        for key, value in validated_data.items():
            if key == "category":
                if not isinstance(value, list):  # Ensure value is a list
                    raise serializers.ValidationError("Category must be a list of ObjectIds.")
                
                try:
                    # Convert category IDs to ObjectId format
                    category_ids = [ObjectId(cid) for cid in value]
                except Exception:
                    raise serializers.ValidationError("Invalid category ID format.")
                
                categories = ProductCategory.objects(id__in=category_ids)
                if len(categories) != len(category_ids):
                    raise serializers.ValidationError("Some categories are invalid.")
                
                instance.category = list(categories)
            else:
                setattr(instance, key, value)
        
        instance.save()
        return instance

    def to_representation(self, instance):

        data = {
            "id": str(instance.id),
            "name": instance.name,
            "description": instance.description,
            "brand": instance.brand,
            "category": [cat.title for cat in instance.category] if instance.category else [],
            "price": float(instance.price),
            "quantity": int(instance.quantity),
        }
        return data
