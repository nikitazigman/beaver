from beaver_api.models import TimeStampMixin, UUIDMixin
from django.db import models


class Tag(UUIDMixin, TimeStampMixin):  # type: ignore
    name: models.CharField = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
