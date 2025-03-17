from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Product 

class ProductSerializer(DocumentSerializer):
    class Meta:
        model = Product
        fields = '__all__'