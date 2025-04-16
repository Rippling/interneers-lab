from rest_framework import serializers
from django_app.models.product import Product
from django_app.models.category import Category
from bson import ObjectId


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(
        required = True,
        max_length = 100,
        allow_blank = False,
        error_messages = {
            "required": "Title is required.",
            "blank":  "Title cannot be empty",
            "max_length": "Title must be at most 100 characters long."
        }
    )

    category = serializers.CharField(
        required = True, 
        allow_blank = False,
        error_messages={
            "required": "Description is required.",
            "blank": "Description cannot be empty."
        }
    )

    description = serializers.CharField(
        required = True, 
        allow_blank = False,
        error_messages={
            "required": "Description is required.",
            "blank": "Description cannot be empty."
        }
    )
    price = serializers.FloatField(
        required = True, 
        min_value = 0.01,
        error_messages = {
            "required": "Price is required.",
            "min_value": "Price cannot be less than 0.01"
        }
    )
    brand = serializers.CharField(
        required = True, 
        allow_blank = False,
        error_messages = {
            "required": "Brand is required.",
            "blank": "Brand cannot be empty."
        }
    )
    quantity = serializers.IntegerField(
        required = True, 
        min_value = 0,
        error_messages = {
            "required": "Quantity is required.",
            "min_value": "Quantity cannot be less than 0."
        }
    )

    created_at = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M:%S"
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M:%S"
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        category_obj = Category.objects(id=instance.category.id).first()
        data["category"] = category_obj.title
        return data
    
    def to_internal_value(self, data):

        errors = {}

        name = data.get("name")
        product_id = self.instance['id'] if self.instance else None
        if name and not errors.get("name"):
            existing_product = Product.objects(name=name).first()
            if existing_product and str(existing_product.id)!=str(product_id):
                errors["name"] = ["A product with this name already exists."]

        category_title = data.get("category")
        category_obj = Category.objects(title=category_title).first()
        if not category_obj:
            errors["category"] = [f"Category '{category_title}' does not exist."]

        try:
            validated_data = super().to_internal_value(data)
        except serializers.ValidationError as e:
            errors.update(e.detail)

        allowed_fields = set(self.fields.keys())
        received_fields = set(data.keys())
        extra_fields = received_fields - allowed_fields
        if extra_fields:
            errors["extra_fields"] = [f"Unexpected fields: {', '.join(extra_fields)}"]

        if errors:
            raise serializers.ValidationError(errors)
        validated_data["category"] = ObjectId(category_obj.id)
        return validated_data