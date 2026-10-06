from rest_framework import serializers


# cheking for category API
class ProductCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(
        required=False, allow_blank=True, default="", max_length=300)
    # output fields only
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # check whether title is not empty
    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value


# checking for products API
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    # here brand is made compulsary not optional
    brand = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    # client need not send whole data just say attach it to category number 1
    category_id = serializers.IntegerField(required=False, allow_null=True)
    # category is nested output field
#      {
#         "id": 1,
#         "name": "Rice",
#         "brand": "India Gate",
#         "category_id": 2,
#         "category": { this is from nested giving better output
#           "id": 2,
#           "title": "Food",
#           "description": "Daily grocery items"
#          }
#       }
    category = ProductCategorySerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    # custom serialization
    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        return value

    def validate_description(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value

    def validate_brand(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Brand is required.")
        return value


# for API like add product to category or remove from category
class ProductCategoryActionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "product_id must be a positive integer.")
        return value
