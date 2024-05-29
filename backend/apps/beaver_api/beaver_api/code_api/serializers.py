from uuid import UUID

from code_api.models import CodeDocument
from code_api.services import (
    compute_hash,
    delete_objects_by_ids,
    get_or_create_obj_by_names,
)

from django.db.models import QuerySet
from language_api.models import Language
from rest_framework import serializers
from tags_api.models import Tag


def check_ids_existence(
    ids: list[UUID], queryset: QuerySet[CodeDocument]
) -> None:
    code_docs = queryset.filter(id__in=ids)
    if len(ids) != code_docs.count():
        raise serializers.ValidationError(
            "Some of the ids does not exist in db"
        )


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
            data["code_content_hash"] = compute_hash(data["code"])
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

    def update(
        self, instance: QuerySet[CodeDocument], validated_data: list[dict]
    ):
        ids = [item["id"] for item in validated_data]
        check_ids_existence(ids=ids, queryset=instance)
        delete_objects_by_ids(instance, ids)
        return self.create(validated_data)


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
    link_to_project = serializers.URLField()

    class Meta:
        model = CodeDocument
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
        list_serializer_class = CodeDocumentListSerializer


class CodeDocumentLimitedContentSerializer(CodeDocumentSerializer):
    class Meta:
        model = CodeDocument
        fields = ["id", "title", "language", "tags", "code_content_hash"]
        read_only_fields = fields


class CodeDocumentDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.UUIDField())

    def validate_ids(self, value: list[UUID]) -> list[UUID]:
        if not value:
            raise serializers.ValidationError("The list of ids is empty.")

        if len(value) != CodeDocument.objects.filter(id__in=value).count():
            raise serializers.ValidationError("Some of the ids are invalid.")

        return value
