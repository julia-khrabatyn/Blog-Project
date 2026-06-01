from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractBaseModel, SlugMixin

__all__ = ("Tag",)


class Tag(AbstractBaseModel, SlugMixin):
    """Represent Tag object"""

    title = models.CharField(
        max_length=50, verbose_name=_("Title"), help_text=_("Tag title")
    )

    def __str__(self):
        return self.title.lower()

    class Meta:
        ordering = ["title"]
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        indexes = [models.Index(fields=["title"])]
