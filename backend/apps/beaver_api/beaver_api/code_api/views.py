from code_api.mixins import GetRandomObjectMixin
from code_api.models import CodeDocument
from code_api.serializers import (
    CodeDocumentSerializer,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class GetRandomCodeDocumentView(GenericAPIView, GetRandomObjectMixin):
    queryset = CodeDocument.objects.all()
    serializer_class = CodeDocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["language__name", "tags__name"]
    pagination_class = None

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.get_random_document(request, *args, **kwargs)
