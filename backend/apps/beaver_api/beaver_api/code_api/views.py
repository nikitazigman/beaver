from code_api.filters import CodeDocumentFilter
from code_api.mixins import GetRandomObjectMixin
from code_api.models import CodeDocument
from code_api.paginators import CodeDocumentPagination
from code_api.serializers import (
    CodeDocumentSerializer,
)

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.exceptions import ValidationError
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

class CodeDocumentCreateView(generics.CreateAPIView):
    serializer_class = CodeDocumentSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CodeDocumentUpdateView(generics.UpdateAPIView):
    serializer_class = CodeDocumentSerializer

    def put(self, request, *args, **kwargs):
        with transaction.atomic():
            for item_data in request.data:
                instance = CodeDocument.objects.get(id=item_data['id'])
                serializer = CodeDocumentSerializer(instance, data=item_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response(status=status.HTTP_200_OK)


class CodeDocumentDeleteView(generics.DestroyAPIView):
    serializer_class = CodeDocumentSerializer

    def delete(self, request: Request, *args, **kwargs):
        ids = request.data.get("ids", [])
        if not ids:
            raise ValidationError("No 'ids' provided for deletion.")
        CodeDocument.objects.filter(id__in=ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CodeDocumentListView(generics.ListAPIView):
    queryset = CodeDocument.objects.all()
    serializer_class = CodeDocumentSerializer
    pagination_class = CodeDocumentPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["title"]
    filterset_class = CodeDocumentFilter
