from django.db import models
from django.utils.text import slugify
from uuid6 import uuid7


class UUIdMixin(models.Model):
    """Mixin that added UUID PK to models"""

    id = models.UUIDField(default=uuid7, primary_key=True, editable=False)

    class Meta:
        abstract = True


class AbstractBaseModel(UUIdMixin):
    """
    Abstract base model with created_at and
    updated_at fields for other models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishMixin(models.Model):
    """Mixin that added published field to model for Multiple inheritance."""

    published = models.BooleanField(default=False)

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    """Mixin that added auto-generated slug field."""

    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="URL-friendly version of the title",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
