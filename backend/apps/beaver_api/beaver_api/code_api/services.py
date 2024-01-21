from random import choice
from typing import TypeVar
from uuid import UUID

from django.db.models import Model, QuerySet
from django.http import Http404


T = TypeVar("T", bound=Model)


def get_random_object_id(queryset: QuerySet) -> UUID:
    objects_ids = queryset.values_list("id", flat=True)

    if not objects_ids:
        raise Http404(
            "No %s matches the given query." % queryset.model._meta.object_name
        )

    random_id = choice(objects_ids)
    return random_id
