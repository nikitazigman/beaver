from contributors.models import Contributor
from rest_framework import serializers


class ContributorBulkSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    address = serializers.EmailField(required=True, allow_blank=False, allow_null=False)


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = Contributor
        fields: tuple = (
            "id",
            "name",
            "last_name",
            "address",
        )
        read_only_fields: tuple = (
            "id",
            "name",
            "last_name",
            "address",
        )
