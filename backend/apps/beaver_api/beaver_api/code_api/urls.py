from code_api.views import (
    CodeDocumentCreateView,
    CodeDocumentDeleteView,
    CodeDocumentListView,
    CodeDocumentUpdateView,
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
        CodeDocumentCreateView.as_view(),
        name="code-document-bulk-create",
    ),
    path(
        "bulk_update/",
        CodeDocumentUpdateView.as_view(),
        name="code-document-bulk-update",
    ),
    path(
        "bulk_delete/",
        CodeDocumentDeleteView.as_view(),
        name="code-document-bulk-delete",
    ),
    path(
        "code_documents/",
        CodeDocumentListView.as_view(),
        name="code-documents-list",
    ),
]
