from code_api.models import CodeDocument
from code_api.services import (
    get_or_create_obj_by_names,
)
from contributors.serializers import (
    ContributorBulkSerializer,
    ContributorSerializer,
)
from django.db.models import Model
from language_api.models import Language
from rest_framework import serializers
from tags_api.models import Tag


class CodeDocumentListSerializer(serializers.ListSerializer):
    def get_tag_mappings(self, validated_data: list[dict]) -> dict[str, Tag]:
        tag_names = set()
        for data in validated_data:
            tag_names.update(data["tags"])

        tags: list[Tag] = get_or_create_obj_by_names(
            names=list(tag_names), model_class=Tag
        )
        return {tag.name: tag for tag in tags}

    def get_language_mappings(
        self, validated_data: list[dict]
    ) -> dict[str, Language]:
        language_names = set(data["language"] for data in validated_data)
        languages: list[Language] = get_or_create_obj_by_names(
            names=list(language_names), model_class=Language
        )
        return {language.name: language for language in languages}

    def create_code_objects(
        self,
        data: dict,
        language_mapping: dict[str, Language],
    ) -> CodeDocument:
        return CodeDocument(
            language=language_mapping[data["language"]],
            title=data["title"],
            code=data["code"],
            link_to_project=data["link_to_project"],
            last_synchronization=data["last_synchronization"],
        )

    def create_code_through_tags(
        self,
        code_object: CodeDocument,
        data: dict,
        tag_mapping: dict[str, Tag],
    ) -> list[Model]:
        return [
            CodeDocument.tags.through(
                codedocument_id=code_object.id,
                tag_id=tag_mapping[tag_name].id,
            )
            for tag_name in data["tags"]
        ]

    def bulk_create_code_docs(
        self,
        tag_mapping: dict[str, Tag],
        language_mapping: dict[str, Language],
        validated_data: list[dict],
    ) -> list[CodeDocument]:
        code_objects: list[CodeDocument] = []
        code_through_tags: list = []

        for data in validated_data:
            code_doc: CodeDocument = self.create_code_objects(
                data=data, language_mapping=language_mapping
            )
            code_objects.append(code_doc)

            through_objects: list[Model] = self.create_code_through_tags(
                code_object=code_doc, data=data, tag_mapping=tag_mapping
            )
            code_through_tags.extend(through_objects)

        new_code_docs: list[CodeDocument] = CodeDocument.objects.bulk_create(
            objs=code_objects
        )
        CodeDocument.tags.through.objects.bulk_create(code_through_tags)

        return new_code_docs

    def create(self, validated_data: list[dict]) -> list[CodeDocument]:
        tag_mapping: dict[str, Tag] = self.get_tag_mappings(
            validated_data=validated_data
        )
        language_mapping: dict[str, Language] = self.get_language_mappings(
            validated_data=validated_data
        )

        return self.bulk_create_code_docs(
            tag_mapping=tag_mapping,
            language_mapping=language_mapping,
            validated_data=validated_data,
        )


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
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:  # type: ignore
        model = CodeDocument
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created_at", "updated_at")
        list_serializer_class = CodeDocumentListSerializer


class CodeDocumentBulkSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)
    tags = serializers.ListField(child=serializers.CharField())
    language = serializers.CharField()
    link_to_project = serializers.CharField()
    contributors = serializers.ListField(
        child=ContributorBulkSerializer(), required=False
    )

    class Meta:  # type: ignore
        model = CodeDocument
        fields: str = "__all__"
        read_only_fields: tuple = ("id", "created_at", "updated_at")
        list_serializer_class = CodeDocumentListSerializer


class CodeDocumentDeleteSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
