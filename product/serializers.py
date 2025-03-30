from rest_framework import serializers
from .models.ProductModel import Product
from .models.CategoryModel import ProductCategory
from datetime import datetime,timezone      #for handling timestamps
from bson import ObjectId

class ProductSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField(required=True,max_length=200)
    description=serializers.CharField(required=False)
    price=serializers.DecimalField(max_digits=10,decimal_places=2)
    category = serializers.PrimaryKeyRelatedField(
        queryset=ProductCategory.objects.all(),
        required=True
    )
    brand=serializers.CharField(required=True,min_length=1)
    quantity=serializers.IntegerField(required=True)
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)

    #validation for brand field
    def validate_brand(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Brand cannot be empty")
        return value
    
    #conversion of ObjectId field to string for response
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)    
        return data
    
#serializer for prod. history track
class ProductHistorySerializer(serializers.Serializer):
    product_id=serializers.CharField()
    name=serializers.CharField()
    description=serializers.CharField()
    category=serializers.CharField()
    price=serializers.DecimalField(max_digits=10,decimal_places=2)
    brand=serializers.CharField()
    quantity=serializers.IntegerField()
    version_created_at=serializers.DateTimeField()    

#method to create a new prod. history
    def create(self, valid_data):
        now=datetime.now(timezone.utc) 
        valid_data['created_at']=now
        valid_data['updated_at']=now
        return Product(**valid_data).save()

#method to update existing prod. history
    def update(self, instance, valid_data):
        for attr, value in valid_data.items():
            setattr(instance, attr, value)
        instance.updated_at=datetime.now(timezone.utc) 
        instance.save()
        return instance
    
#serializer for prod. category model
class ProductCategorySerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    title=serializers.CharField(max_length=100)
    description=serializers.CharField(required=False, allow_blank=True)
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return ProductCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance