from django.db import models
from django.utils.text import slugify
from uuid6 import uuid7

__all__ = ("AbstractBaseModel", "PublishMixin", "SlugMixin", "UUIdMixin")


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

    def generate_unique_slug(self):
        source = self.slug or self.title
        base_slug = slugify(source)

        if not base_slug:
            base_slug = "item"

        slug = base_slug
        num = 1
        model = self.__class__

        while model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug

    def save(self, *args, **kwargs):
        # Additional uniqueness check before saving
        self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
