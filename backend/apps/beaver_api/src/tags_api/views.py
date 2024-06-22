from tags_api.models import Tag
from tags_api.serializers import TagSerializer

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


class ListTagView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
