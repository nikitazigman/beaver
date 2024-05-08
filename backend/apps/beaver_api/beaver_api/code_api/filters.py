from code_api.models import CodeDocument

from django_filters.rest_framework import CharFilter, FilterSet


class CodeDocumentFilter(FilterSet):
    tags = CharFilter(field_name="tags__name", lookup_expr="icontains")

    class Meta:
        model = CodeDocument
        fields = ["tags"]
