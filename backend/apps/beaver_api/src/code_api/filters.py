import django_filters

from code_api.models import CodeDocument


class CodeDocumentFilter(django_filters.FilterSet):
    class Meta:
        model = CodeDocument
        fields = {
            'language__name': ['exact'],
            'tags__name': ['in'],
        }

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)

        language = request.GET.get("language") if request else None
        tags = request.GET.getlist("tags") if request else None

        if language:
            self.queryset = self.queryset.filter(language__name=language)
        if tags:
            self.queryset = self.queryset.filter(tags__name__in=tags)
