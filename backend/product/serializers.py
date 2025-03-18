from rest_framework import serializers
from .models import Product
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

    def to_representation(self, instance):
        """Convert MongoEngine document to JSON serializable format."""
        data = super().to_representation(instance)
        data['id'] = str(instance.id) if isinstance(instance.id, ObjectId) else instance.id
        return data

    def create(self, validated_data):
        """Create a new product."""
        return Product(**validated_data).save()

    def update(self, instance, validated_data):
        """Update an existing product."""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
