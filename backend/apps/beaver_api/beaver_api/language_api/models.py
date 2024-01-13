from beaver_api.models import TimeStampMixin, UUIDMixin
from django.db import models


class Language(UUIDMixin, TimeStampMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Create your models here.
