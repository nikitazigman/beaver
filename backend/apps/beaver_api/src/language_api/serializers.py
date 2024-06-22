from language_api.models import Language

from rest_framework.serializers import ModelSerializer


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = (
            "id",
            "name",
        )
        read_only_fields = (
            "id",
            "name",
        )
