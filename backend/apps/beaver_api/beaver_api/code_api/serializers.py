from code_api.models import CodeDocument

from rest_framework import serializers


class CodeDocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CodeDocument
        fields = (
            "id",
            "title",
            "code",
            "link_to_project",
            "language",
            "tags",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
