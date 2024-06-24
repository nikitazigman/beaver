from language_api.views import ListLanguageView

from django.urls import path


urlpatterns = [
    path("", ListLanguageView.as_view(), name="list-language"),
]
