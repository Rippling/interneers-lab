from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework import serializers
from product.models.product import Product

class ProductSerializer(DocumentSerializer):
    # Explicitly override the brand field
    brand = serializers.CharField(
        required=True,
        max_length=50,
        # error_messages={'required': 'Please provide a brand name.',
        #                 'blank': 'Brand cannot be blank'}  # Custom message for missing field
    )

    class Meta:
        model = Product
        fields = '__all__'
        
    def validate_price(self, value):
        if value > 1000:
            raise serializers.ValidationError("Price should be less than 1000")
        return value
    
    def validate_quantity(self, value):
        if value < 10:
            raise serializers.ValidationError("Quantity should not be lesser than 10")
        return value
