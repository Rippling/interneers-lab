from rest_framework import serializers
from .models import Product
from .utils import convert_utc_to_ist  
from bson import ObjectId

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(max_length=255)
    price_in_RS = serializers.FloatField()
    brand = serializers.CharField(required=False, allow_blank=True)
    quantity = serializers.IntegerField()
    manufacture_date = serializers.DateField()
    expiry_date = serializers.DateField()
    weight_in_KG = serializers.FloatField(required=False, default=0.0)

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
        """Creates a new product, ensuring timestamps are auto-set."""
        product = Product(**validated_data)
        product.save()  
        return product

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()  
        return instance
