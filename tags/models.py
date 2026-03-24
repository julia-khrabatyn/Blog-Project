from django.db import models

from core.models import AbstractBaseModel, SlugMixin

__all__ = ("Tag",)


class Tag(AbstractBaseModel, SlugMixin):
    """Represent Tag object"""

    title = models.CharField(max_length=50, help_text="Tag title")

    def __str__(self):
        return self.title.lower()

    class Meta:
        ordering = ["title"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        indexes = [models.Index(fields=["title"])]
