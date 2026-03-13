from django.db import models
from core.models import AbstractBaseModel

# Create your models here.


class Comment(AbstractBaseModel):
    """Represent comments."""

    text = models.TextField()
    post = models.ForeignKey(
        "blog.Post", on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"{self.user} leave a comment on {self.post}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["user"]),
        ]
