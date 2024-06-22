from language_api.models import Language
from language_api.serializers import LanguageSerializer

from rest_framework.generics import ListAPIView


class ListLanguageView(ListAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
