from tags_api.views import ListTagView

from django.urls import path


urlpatterns = [
    path("", ListTagView.as_view(), name="list-tag"),
]
