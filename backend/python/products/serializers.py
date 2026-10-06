from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
        def validate_name(self,value):
            if len(value)<3:
                raise serializers.ValidationError("Product name must be at least 3 characters long.")
            return value