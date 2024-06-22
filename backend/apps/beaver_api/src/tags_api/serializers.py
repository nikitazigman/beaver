from tags_api.models import Tag

from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
        )
        read_only_fields = (
            "id",
            "name",
        )
