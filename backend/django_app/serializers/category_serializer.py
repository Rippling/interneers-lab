from rest_framework import serializers
from django_app.models.category import Category

class CategorySerializer(serializers.Serializer):

    id = serializers.CharField(read_only=True)
    title = serializers.CharField(
        required = True, 
        allow_blank = False, 
        max_length = 100,
        error_messages = {
            "required": "Title is required.",
            "blank":  "Title cannot be empty",
            "max_length": "Title must be at most 100 characters long."
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

    created_at = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M:%S"
    )
    updated_at = serializers.DateTimeField(
        read_only=True,
        format="%Y-%m-%d %H:%M:%S"
    )

    def to_internal_value(self, data):

        errors = {}

        title = data.get("title")
        category_id = self.instance['id'] if self.instance else None
        if title and not errors.get("title"):
            existing_product = Category.objects(title=title).first()
            if existing_product and str(existing_product.id)!=str(category_id):
                errors["title"] = [f"A category with title '{title}' already exists."]

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
        return validated_data