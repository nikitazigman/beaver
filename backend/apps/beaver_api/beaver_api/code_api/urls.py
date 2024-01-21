from code_api.views import GetRandomCodeDocumentView

from django.urls import path


urlpatterns = [
    path(
        "code_documents/",
        GetRandomCodeDocumentView.as_view(),
        name="code_documents",
    ),
]
