from datetime import datetime
from typing import TypeVar

from code_api.models import CodeDocument
from django.db.models import Model, QuerySet


T = TypeVar("T", bound=Model)


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
