from code_api.views import (
    CodeDocumentBulkDeleteView,
    CodeDocumentBulkUpdateView,
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
        "bulk_update/",
        CodeDocumentBulkUpdateView.as_view(),
        name="code-document-bulk-update",
    ),
    path(
        "bulk_delete/",
        CodeDocumentBulkDeleteView.as_view(),
        name="code-document-bulk-delete",
    ),
]
