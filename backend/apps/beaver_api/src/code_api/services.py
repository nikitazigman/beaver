from datetime import datetime
from typing import TypeVar

from code_api.models import CodeDocument
from contributors.models import Contributor
from django.db.models import Model, QuerySet
from tags_api.models import Tag


T = TypeVar("T", bound=Model)


def bulk_get_or_create_obj_by_names(names: list[str], model_class: type[T]) -> list[T]:
    existing_objs: QuerySet[T] = model_class.objects.filter(name__in=names)
    existing_names: set[str] = set(existing_objs.values_list("name", flat=True))

    new_names: set[str] = set(names) - existing_names

    new_obj_instances: list[T] = [model_class(name=name) for name in new_names]
    new_objs: list[T] = model_class.objects.bulk_create(objs=new_obj_instances)

    return list(existing_objs) + new_objs


def bulk_ger_or_create_contributors(contributors: list[dict]) -> list[Contributor]:
    contributor_mapping: dict[str, dict] = {contributor["address"]: contributor for contributor in contributors}
    existing_contributors: QuerySet[Contributor] = Contributor.objects.filter(address__in=contributor_mapping.keys())
    existing_addresses = set(existing_contributors.values_list("address", flat=True))
    contributors_to_create: set[str] = set(contributor_mapping.keys()) - existing_addresses
    new_contributors_instances: list[Contributor] = [
        Contributor(**contributor_mapping[address]) for address in contributors_to_create
    ]
    new_contributors: list[Contributor] = Contributor.objects.bulk_create(objs=new_contributors_instances)

    return list(existing_contributors) + new_contributors


def delete_docs_before_timestamp(timestamp: datetime, queryset: QuerySet[CodeDocument]) -> None:
    docs_to_delete: QuerySet[CodeDocument] = queryset.filter(last_synchronization__lt=timestamp)
    docs_to_keep: QuerySet[CodeDocument] = queryset.exclude(last_synchronization__lt=timestamp)
    tags_to_delete: QuerySet[Tag] = Tag.objects.exclude(code_documents__in=docs_to_keep)
    contributors_to_delete: QuerySet[Contributor] = Contributor.objects.exclude(code_documents__in=docs_to_keep)

    tags_to_delete.delete()
    contributors_to_delete.delete()
    docs_to_delete.delete()
