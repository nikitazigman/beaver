from code_api.mixins import GetRandomObjectMixin
from code_api.models import CodeDocument
from code_api.paginators import CodeDocumentPagination
from code_api.serializers import (
    CodeDocumentBulkSerializer,
    CodeDocumentDeleteSerializer,
    CodeDocumentLimitedContentSerializer,
    CodeDocumentSerializer,
)
from code_api.services import delete_objects_by_ids

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
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


class CodeDocumentBulkCreateView(generics.CreateAPIView):
    serializer_class = CodeDocumentBulkSerializer

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class CodeDocumentBulkUpdateView(generics.GenericAPIView):
    serializer_class = CodeDocumentBulkSerializer
    queryset = CodeDocument.objects.all()

    @transaction.atomic
    def post(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset, data=request.data, many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update()

        return Response(status=status.HTTP_200_OK)


class CodeDocumentBulkDeleteView(generics.DestroyAPIView):
    serializer_class = CodeDocumentDeleteSerializer
    queryset = CodeDocument.objects.all()

    def delete(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delete_objects_by_ids(self.queryset, serializer.validated_data["ids"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class CodeDocumentListView(generics.ListAPIView):
    queryset = (
        CodeDocument.objects.seal()
        .select_related("language")
        .prefetch_related("tags")
        .all()
    )
    serializer_class = CodeDocumentLimitedContentSerializer
    pagination_class = CodeDocumentPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["title"]
