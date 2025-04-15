from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    price=serializers.FloatField()
