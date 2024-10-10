from beaver_api.models import TimeStampMixin, UUIDMixin
from django.db import models
from language_api.models import Language
from seal.models import SealableModel
from tags_api.models import Tag


class CodeDocument(UUIDMixin, TimeStampMixin, SealableModel):  # type: ignore
    title: models.CharField = models.CharField(
        max_length=255, blank=False, null=False, unique=True
    )
    code: models.TextField = models.TextField(blank=False, null=False)
    link_to_project: models.URLField = models.URLField(
        blank=False, null=False, unique=False
    )

    language: models.ForeignKey = models.ForeignKey(
        Language,
        on_delete=models.DO_NOTHING,
        related_name="code_documents",
        null=True,
    )
    tags: models.ManyToManyField = models.ManyToManyField(
        Tag, related_name="code_documents"
    )
    last_synchronization: models.DateTimeField = models.DateTimeField(
        null=False, blank=False
    )

    def __str__(self) -> str:
        return f"{self.language}/{self.title}"
