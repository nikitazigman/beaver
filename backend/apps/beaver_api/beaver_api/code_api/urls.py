from code_api.views import (
    CodeDocumentBulkCreateView,
    CodeDocumentBulkDeleteView,
    CodeDocumentBulkUpdateView,
    CodeDocumentListView,
    GetRandomCodeDocumentView,
)

from django.urls import path


urlpatterns = [
    path(
        "code_document/",
        GetRandomCodeDocumentView.as_view(),
        name="code_document",
    ),
    path(
        "bulk_create/",
        CodeDocumentBulkCreateView.as_view(),
        name="code-document-bulk-create",
    ),
    path(
        "bulk_update/",
        CodeDocumentBulkUpdateView.as_view(),
        name="code-document-bulk-update",
    ),
    path(
        "bulk_delete/",
        CodeDocumentBulkDeleteView.as_view(),
        name="code-document-bulk-delete",
    ),
    path(
        "code_documents/",
        CodeDocumentListView.as_view(),
        name="code-documents-list",
    ),
]
