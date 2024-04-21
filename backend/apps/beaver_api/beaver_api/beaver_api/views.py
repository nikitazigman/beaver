from hashlib import sha256

from beaver_api.filters import CodeDocumentFilter
from beaver_api.paginators import CodeDocumentPagination

from code_api.models import CodeDocument, Tag
from code_api.serializers import CodeDocumentSerializer
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response


class BaseCodeDocumentView(generics.GenericAPIView):
    serializer_class = CodeDocumentSerializer

    def compute_hash_for_code(self, item):
        code_content = item.get("code")
        if code_content:
            return sha256(code_content.encode("utf-8")).hexdigest()
        return None


class CodeDocumentCreateView(BaseCodeDocumentView):
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        for item in serializer.validated_data:
            item["code_content_hash"] = self.compute_hash_for_code(item)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CodeDocumentUpdateView(BaseCodeDocumentView):
    def put(self, request: Request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            updated_objects = []
            for code_document_data in serializer.validated_data:
                try:
                    code_document_instance = CodeDocument.objects.get(
                        id=code_document_data["id"]
                    )
                except CodeDocument.DoesNotExist:
                    raise ValidationError(
                        f"Code document with id {code_document_data['id']} "
                        "does not exist."
                    )

                code_content_hash = self.compute_hash_for_code(
                    code_document_data
                )
                code_document_instance.code_content_hash = code_content_hash

                tags = []
                for tag_name in code_document_data.get("tags", []):
                    tag_instance = Tag.objects.get(name=tag_name)
                    tags.append(tag_instance)
                code_document_instance.tags.set(tags)

                for field, value in code_document_data.items():
                    if field not in ["id", "tags"]:
                        setattr(code_document_instance, field, value)

                code_document_instance.save()
                updated_objects.append(code_document_instance)

            response_serializer = CodeDocumentSerializer(
                updated_objects, many=True
            )
            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )


class CodeDocumentDeleteView(BaseCodeDocumentView):
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
