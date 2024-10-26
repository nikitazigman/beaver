from language_api.models import Language
from rest_framework.serializers import ModelSerializer


class LanguageSerializer(ModelSerializer):
    class Meta:  # type: ignore
        model = Language
        fields: tuple = (
            "id",
            "name",
        )
        read_only_fields: tuple = (
            "id",
            "name",
        )
