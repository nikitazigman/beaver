from code_api.models import CodeDocument
from code_api.services import (
    get_or_create_obj_by_names,
)

from language_api.models import Language
from rest_framework import serializers
from tags_api.models import Tag


class CodeDocumentListSerializer(serializers.ListSerializer):
    # TODO: Refactor
    def create(self, validated_data: list[dict]) -> list[CodeDocument]:
        tag_names = set()
        for data in validated_data:
            tag_names.update(data["tags"])
        tags: list[Tag] = get_or_create_obj_by_names(
            names=list(tag_names), model_class=Tag
        )
        tag_mapping = {tag.name: tag for tag in tags}

        language_names = set(data["language"] for data in validated_data)
        languages: list[Language] = get_or_create_obj_by_names(
            names=list(language_names), model_class=Language
        )
        language_mapping = {language.name: language for language in languages}

        code_objects: list[CodeDocument] = []
        code_through_tags: list[CodeDocument.tags.through] = []
        for data in validated_data:
            data["language"] = language_mapping[data["language"]]
            tags = data.pop("tags")
            code_doc = CodeDocument(**data)
            code_objects.append(code_doc)
            through_objects = [
                CodeDocument.tags.through(
                    codedocument_id=code_doc.id,
                    tag_id=tag_mapping[tag_name].id,
                )
                for tag_name in tags
            ]
            code_through_tags.extend(through_objects)

        new_code_docs = CodeDocument.objects.bulk_create(code_objects)
        CodeDocument.tags.through.objects.bulk_create(code_through_tags)

        return new_code_docs


class CodeDocumentSerializer(serializers.ModelSerializer):
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
    link_to_project = serializers.URLField()

    class Meta:
        model = CodeDocument
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        list_serializer_class = CodeDocumentListSerializer


class CodeDocumentBulkSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    tags = serializers.ListField(child=serializers.CharField())
    language = serializers.CharField()
    link_to_project = serializers.CharField()

    class Meta:
        model = CodeDocument
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        list_serializer_class = CodeDocumentListSerializer


class CodeDocumentDeleteSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
