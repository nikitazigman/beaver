from django.urls import path
from tags_api.views import ListTagView


urlpatterns = [
    path("", ListTagView.as_view(), name="list-tag"),
]
