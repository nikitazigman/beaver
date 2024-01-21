from typing import Protocol

from django.db.models import QuerySet
from rest_framework.serializers import BaseSerializer


class GenericViewProtocol(Protocol):
    def get_queryset(self):
        ...

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        ...

    def get_serializer(self, *args, **kwargs) -> BaseSerializer:
        ...
