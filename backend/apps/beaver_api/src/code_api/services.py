from datetime import datetime
from typing import TypeVar

from code_api.models import CodeDocument
from django.db.models import Model, QuerySet


T = TypeVar("T", bound=Model)


def get_or_create_obj_by_names(
    names: list[str], model_class: type[T]
) -> list[T]:
    existing_objs: QuerySet[T] = model_class.objects.filter(name__in=names)
    existing_names: set[str] = set(
        existing_objs.values_list("name", flat=True)
    )

    new_names: set[str] = set(names) - existing_names

    new_obj_instances: list[T] = [model_class(name=name) for name in new_names]
    new_objs: list[T] = model_class.objects.bulk_create(objs=new_obj_instances)

    return list(existing_objs) + new_objs


def delete_docs_before_timestamp(
    timestamp: datetime, queryset: QuerySet[CodeDocument]
) -> None:
    docs_to_delete: QuerySet[CodeDocument] = queryset.filter(
        last_synchronization__lt=timestamp
    )
    docs_to_delete.delete()
