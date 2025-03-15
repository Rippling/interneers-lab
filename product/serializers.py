from rest_framework import serializers
from .models import Product
from datetime import datetime,timezone      #for handling timestamps

#serializer for prod. model
class ProductSerializer(serializers.Serializer):
    id=serializers.CharField(read_only=True)
    name=serializers.CharField(required=True,max_length=200)
    description=serializers.CharField(required=False)
    price=serializers.DecimalField(max_digits=10, decimal_places=2)
    category=serializers.CharField(required=False)
    brand=serializers.CharField(required=True)
    quantity=serializers.IntegerField(required=True)
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)

#serializer for prod. history track
class ProductHistorySerializer(serializers.Serializer):
    product_id=serializers.CharField()
    name=serializers.CharField()
    description=serializers.CharField()
    category=serializers.CharField()
    price=serializers.DecimalField(max_digits=10, decimal_places=2)
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