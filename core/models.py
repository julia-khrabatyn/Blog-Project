from django.db import models


# Create your models here.
class AbstractBaseModel(models.Model):
    """
    Abstract base model with created_at and
    updated_at fields for other models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        # ordering = ["-created_at"]
