from beaver_api.models import TimeStampMixin, UUIDMixin
from django.db import models


class Contributor(TimeStampMixin, UUIDMixin):  # type: ignore
    name: models.CharField = models.CharField(max_length=256)
    last_name: models.CharField = models.CharField(max_length=256)
    address: models.EmailField = models.EmailField(max_length=256)
