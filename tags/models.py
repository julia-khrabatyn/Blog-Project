from django.db import models
from core.models import AbstractBaseModel


# Create your models here.
class Tag(AbstractBaseModel):
    """Represent Tag object"""

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title.lower()

    class Meta:
        ordering = ["title"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        indexes = [models.Index(fields=["title"])]
