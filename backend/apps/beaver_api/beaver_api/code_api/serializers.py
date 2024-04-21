from code_api.models import CodeDocument

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from language_api.models import Language
from rest_framework import serializers
from tags_api.models import Tag


class CodeDocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Tag.objects.all(),
        error_messages={
            "does_not_exist": "Tag with name {value} does not exist."
        },
    )
    language = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Language.objects.all(),
        error_messages={
            "does_not_exist": "Language with name {value} does not exist."
        },
    )

    class Meta:
        model = CodeDocument
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_title(self, value):
        if CodeDocument.objects.filter(title=value).exists():
            raise serializers.ValidationError("Title must be unique.")
        return value

    def validate_code(self, value):
        if CodeDocument.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                "Code snippet already exists in the database."
            )
        return value

    def validate_link_to_project(self, value):
        url_validator = URLValidator()
        try:
            url_validator(value)
        except ValidationError as e:
            raise ValidationError(
                _("Invalid URL format"), code="invalid"
            ) from e

        return value
