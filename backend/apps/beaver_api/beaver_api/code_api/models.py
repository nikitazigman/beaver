from beaver_api.models import TimeStampMixin, UUIDMixin
from django.db import models


class CodeDocument(UUIDMixin, TimeStampMixin):
    title = models.CharField(
        max_length=255, blank=False, null=False, unique=True
    )
    code = models.TextField(blank=False, null=False, unique=True)
    link_to_project = models.URLField(blank=False, null=False, unique=True)

    language = models.ForeignKey(
        "language_api.Language",
        on_delete=models.DO_NOTHING,
        related_name="code_documents",
        null=True,
    )
    tags = models.ManyToManyField(
        "tags_api.Tag", related_name="code_documents"
    )

    def __str__(self):
        return f"{self.language}/{self.title}"
