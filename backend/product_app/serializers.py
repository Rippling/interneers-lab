from rest_framework.serializers import Serializer, CharField, FloatField, IntegerField
from .models import Product
class ProductSerializer(Serializer):
    name = CharField(max_length=255, required=False)
    description = CharField(allow_blank=True, required=False)
    category = CharField(max_length=100, required=False)
    price = FloatField(required=False)
    brand = CharField(max_length=100, required=False)
    quantity = IntegerField(required=False)