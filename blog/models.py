from django.db import models
from core.models import AbstractBaseModel, PublishMixin
from accounts.models import User


# Create your models here.
class Post(AbstractBaseModel, PublishMixin):
    """
    Represent Post
    """

    title = models.CharField(max_length=255)
    text = models.TextField()
    description = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title.title()

    @property
    def short_text(self):
        """
        Get slice from post text for representing.
        """
        return self.text[:100]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["published"]),
            models.Index(fields=["user", "published"]),
            models.Index(fields=["published", "created_at"]),
            models.Index(fields=["user", "published", "created_at"]),
        ]
