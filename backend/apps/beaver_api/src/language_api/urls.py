from django.urls import path
from language_api.views import ListLanguageView


urlpatterns = [
    path("", ListLanguageView.as_view(), name="list-language"),
]
