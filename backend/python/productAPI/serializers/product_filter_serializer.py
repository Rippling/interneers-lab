from rest_framework import serializers


class ProductFilterSerializer(serializers.Serializer):
    category = serializers.CharField(required=False)
    brand = serializers.CharField(required=False)
    
    min_price = serializers.FloatField(required=False, min_value = 0)
    max_price = serializers.FloatField(required=False, min_value = 0)
      
    sort_by = serializers.ChoiceField(
        choices=[
            "desc",
            "asc",
        ],
        default = "desc"
    )    
    
    page_number = serializers.IntegerField(default = 1)
    
    def validate(self, attrs):
        min_price = attrs.get("min_price")
        max_price = attrs.get("max_price")

        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise serializers.ValidationError(
                "min_price cannot exceed max_price"
            )

        return attrs   