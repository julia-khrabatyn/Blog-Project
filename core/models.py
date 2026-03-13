from django.db import models
from uuid6 import uuid7


# Create your models here.
class AbstractBaseModel(models.Model):
    """
    Abstract base model with created_at and
    updated_at fields for other models.
    """

    id = models.UUIDField(default=uuid7, primary_key=True, editable=False)
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
