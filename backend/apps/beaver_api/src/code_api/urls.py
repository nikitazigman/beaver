from code_api.views import (
    CodeDocumentBulkDeleteView,
    CodeDocumentBulkUpdateView,
    GetRandomCodeDocumentView,
)
from django.urls import path
from django.urls.resolvers import URLPattern


urlpatterns: list[URLPattern] = [
    path(route="code_document/", view=GetRandomCodeDocumentView.as_view(), name="code_document"),
    path(route="bulk_update/", view=CodeDocumentBulkUpdateView.as_view(), name="code-document-bulk-update"),
    path(route="bulk_delete/", view=CodeDocumentBulkDeleteView.as_view(), name="code-document-bulk-delete"),
]
