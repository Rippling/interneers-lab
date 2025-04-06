from rest_framework import serializers
from product.models.product_model import Product
from product.utils import convert_utc_to_ist  
from bson import ObjectId
from product.models.category import ProductCategory 

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)  
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    category = serializers.SerializerMethodField()    
    price_in_RS = serializers.FloatField()
    brand = serializers.CharField(required=True, allow_blank=False)
    quantity = serializers.IntegerField()
    manufacture_date = serializers.DateField()
    expiry_date = serializers.DateField()
    weight_in_KG = serializers.FloatField(required=False, default=0.0)

    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)

    def get_category(self, obj):
        """Extracting category names from the list of ProductCategory references"""
        category_names = [category.category_name for category in obj.category] 
        return category_names

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = str(instance.id) if isinstance(instance.id, ObjectId) else instance.id
        
        # Converts timestamps to IST for API response
        data['created_at'] = convert_utc_to_ist(instance.created_at)
        data['updated_at'] = convert_utc_to_ist(instance.updated_at)
        
        return data

    def create(self, validated_data):
        product = Product(**validated_data)
        product.save()  
        return product

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()  
        return instance
