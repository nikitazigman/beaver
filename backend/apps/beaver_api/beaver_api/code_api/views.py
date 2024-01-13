from code_api.models import CodeDocument
from code_api.serializers import (
    CodeDocumentSerializer,
)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView


class RetrieveCodeDocumentView(RetrieveAPIView):
    queryset = CodeDocument.objects.all()
    serializer_class = CodeDocumentSerializer


class ListCodeDocumentView(ListAPIView):
    queryset = CodeDocument.objects.all()
    serializer_class = CodeDocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["language__name", "tags__name"]
