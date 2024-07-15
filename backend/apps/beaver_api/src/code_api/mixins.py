from beaver_api.protocols import GenericViewProtocol
from code_api import services
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response


class GetRandomObjectMixin(GenericViewProtocol):
    cache_timeout_sec = 60 * 60

    def get_random_document(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        object_id = services.get_random_object_id(queryset=queryset)

        if cached_object := cache.get(str(object_id)):
            return Response(cached_object)

        random_object = get_object_or_404(queryset, id=object_id)
        serializer = self.get_serializer(random_object)

        cache.set(
            key=str(object_id),
            value=serializer.data,
            timeout=self.cache_timeout_sec,
        )

        return Response(serializer.data)
