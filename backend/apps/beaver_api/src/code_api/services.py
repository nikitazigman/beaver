from datetime import datetime
from random import choice
from typing import TypeVar
from uuid import UUID

from code_api.models import CodeDocument
from django.db.models import Model, QuerySet
from django.http import Http404


T = TypeVar("T", bound=Model)


def get_random_object_id(queryset: QuerySet) -> UUID:
    objects_ids = queryset.values_list("id", flat=True)

    if not objects_ids:
        raise Http404(
            f"No {queryset.model._meta.object_name} matches the given query."
        )

    random_id = choice(objects_ids)
    return random_id


def get_or_create_obj_by_names[T: Model](
    names: list[str], model_class: T
) -> list[T]:
    existing_objs = model_class.objects.filter(name__in=names)
    existing_names = existing_objs.values_list("name", flat=True)

    new_names = set(names) - set(existing_names)

    new_obj_instances = [model_class(name=name) for name in new_names]
    new_objs = model_class.objects.bulk_create(new_obj_instances)

    return list(existing_objs) + new_objs


def delete_docs_before_timestamp(
    timestamp: datetime, queryset: QuerySet[CodeDocument]
) -> None:
    docs_to_delete = queryset.filter(last_synchronization__lt=timestamp)
    docs_to_delete.delete()
