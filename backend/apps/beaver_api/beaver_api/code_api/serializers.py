import hashlib

from code_api.models import CodeDocument

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from language_api.models import Language
from rest_framework import serializers
from tags_api.models import Tag


class CodeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeDocument
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    id = serializers.UUIDField(required=False)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Tag.objects.all(),
    )
    language = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Language.objects.all(),
    )

    def create(self, validated_data):
        encoded_code_content = validated_data["code"].encode("utf-8")
        hashed_code_content = hashlib.sha256(encoded_code_content).hexdigest()
        validated_data["code_content_hash"] = hashed_code_content
        return super().create(validated_data)

    def update(self, instance: CodeDocument, validated_data):
        tags_data = validated_data.pop("tags", [])

        # Update scalar fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update many-to-many fields
        if tags_data:
            instance.tags.set(tags_data)

        return instance

    def validate_link_to_project(self, value):
        url_validator = URLValidator()
        try:
            url_validator(value)
        except ValidationError as e:
            raise e

        return value
