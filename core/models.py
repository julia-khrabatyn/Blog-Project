from django.db import models
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
        # ordering = ["-created_at"]


class PublishMixin(models.Model):
    """Mixin that added published field to model for Multiple inheritance."""

    published = models.BooleanField(default=False)

    class Meta:
        abstract = True
