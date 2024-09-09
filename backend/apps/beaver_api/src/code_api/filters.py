from typing import Any

import django_filters

from code_api.models import CodeDocument
from django.db.models import QuerySet
from django.http import HttpRequest


class CodeDocumentFilter(django_filters.FilterSet):
    class Meta:
        model = CodeDocument
        fields = {
            "language__name": ["exact"],
            "tags__name": ["in"],
        }

    def __init__(
        self,
        data: dict[str, Any] | None = None,
        queryset: QuerySet[CodeDocument] | None = None,
        *,
        request: HttpRequest | None = None,
        prefix: str | None = None,
    ) -> None:
        super().__init__(data, queryset, request=request, prefix=prefix)

        language: str | None = request.GET.get("language") if request else None
        tags: list[str] = request.GET.getlist("tags") if request else []

        if language:
            self.queryset = self.queryset.filter(language__name=language)
        if tags:
            self.queryset = self.queryset.filter(tags__name__in=tags)
