from rest_framework import serializers
from product.models.category import ProductCategory
from product.utils import convert_utc_to_ist  
from bson import ObjectId

class ProductCategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    category_name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id) if isinstance(instance.id, ObjectId) else instance.id
        
        # Converts timestamps to IST for API response
        data['created_at'] = convert_utc_to_ist(instance.created_at)
        data['updated_at'] = convert_utc_to_ist(instance.updated_at)
        
        return data

    def create(self, validated_data):
        category = ProductCategory(**validated_data)
        category.save()  
        return category

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()  
        return instance
