from code_api.views import ListCodeDocumentView, RetrieveCodeDocumentView

from django.urls import path


urlpatterns = [
    path(
        "code_documents/<uuid:pk>/",
        RetrieveCodeDocumentView.as_view(),
        name="code_document",
    ),
    path(
        "code_documents/",
        ListCodeDocumentView.as_view(),
        name="code_documents",
    ),
]
