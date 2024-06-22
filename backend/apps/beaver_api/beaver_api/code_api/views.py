from code_api.mixins import GetRandomObjectMixin
from code_api.models import CodeDocument
from code_api.serializers import (
    CodeDocumentBulkSerializer,
    CodeDocumentDeleteSerializer,
    CodeDocumentSerializer,
)
from code_api.services import (
    delete_docs_before_timestamp,
)

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
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


class CodeDocumentBulkUpdateView(generics.GenericAPIView):
    serializer_class = CodeDocumentBulkSerializer
    queryset = CodeDocument.objects.all()
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=request.data, many=True)

        titles = [item["title"] for item in request.data]
        queryset.filter(title__in=titles).delete()

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(status=status.HTTP_200_OK)


class CodeDocumentBulkDeleteView(generics.GenericAPIView):
    serializer_class = CodeDocumentDeleteSerializer
    queryset = CodeDocument.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        delete_docs_before_timestamp(
            timestamp=serializer.validated_data["timestamp"],
            queryset=self.queryset,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
