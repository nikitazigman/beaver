import hashlib

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


def delete_objects_by_ids(queryset: QuerySet, ids: list[UUID]) -> None:
    queryset.filter(id__in=ids).delete()


def compute_hash(code: str) -> dict:
    encoded_code_content = code.encode("utf-8")
    return hashlib.sha256(encoded_code_content).hexdigest()


def get_or_create_obj_by_names[T: Model](
    names: list[str], model_class: T
) -> list[T]:
    existing_objs = model_class.objects.filter(name__in=names)
    existing_names = existing_objs.values_list("name", flat=True)

    new_names = set(names) - set(existing_names)

    new_obj_instances = [model_class(name=name) for name in new_names]
    new_objs = model_class.objects.bulk_create(new_obj_instances)

    return list(existing_objs) + new_objs
