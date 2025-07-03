from rest_framework_mongoengine.serializers import DocumentSerializer  # type: ignore 
from rest_framework.serializers import SerializerMethodField, ValidationError
from .models import Products, ProductCategory
from bson import ObjectId
from rest_framework import serializers


class ObjectIdField(serializers.Field):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        try:
            return ObjectId(str(data))
        except Exception:
            raise serializers.ValidationError("Invalid ObjectId format")


# class ProductSerializer(DocumentSerializer):
#      pass  

class ProductSerializer(DocumentSerializer):

    category = serializers.SerializerMethodField()  # for displaying category name in the response
    category_Id = serializers.IntegerField(write_only=True) # for accepting category_id as input
    category_id = serializers.SerializerMethodField() 

    class Meta:
        model = Products
        fields = "__all__"
        read_only_fields = ('created_at', 'updated_at')


    def get_category(self, obj):
        return obj.category.category_name if obj.category else None
    
    def get_category_id(self, obj):
        return obj.category.category_id if obj.category else None

    def create(self, validated_data):
        # Pull category reference
        category_Id = validated_data.pop('category_Id', None)
        try:
            category_obj = ProductCategory.objects.get(category_id=category_Id)
        
        except ProductCategory.DoesNotExist:
            raise ValidationError({"category_id": f"Category with id {category_Id} not found."})
        
        product = Products(**validated_data)
        product.category = category_obj
        product.category_Id = category_Id
        if not product.product_id:
            last_product = Products.objects.order_by('-product_id').first()
            product.product_id = last_product.product_id + 1 if last_product else 1
           
        product.save()
        return product
    
    def validate_brand(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Brand is required and cannot be empty.")
        return value



class ProductCategorySerializer(DocumentSerializer):

    product_list = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        fields = ["category_id", "category_name", "description","product_list"]
        # fields = '__all__'


    def get_product_list(self, obj):
        products = Products.objects(category=obj)
        return ProductSerializer(products,many=True).data

    def create(self, validated_data):
        print("Validated Data:", validated_data)  # 👈 Add this
        return super().create(validated_data)





    # def to_internal_value(self, data):
    #     if "category" in data:
    #         category_id = data["category"]
    #         try:
    #             category_obj = ProductCategory.objects.get(category_id=int(category_id))
    #             data["category"] = category_obj
    #         except ProductCategory.DoesNotExist:
    #             raise ValidationError({"category": f"Category with id {category_id} not found."})
    #     return super().to_internal_value(data)



    