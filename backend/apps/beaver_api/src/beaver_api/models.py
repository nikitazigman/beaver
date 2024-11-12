from uuid import uuid4

from django.db import models


class UUIDMixin(models.Model):
    id: models.UUIDField = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
