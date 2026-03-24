from django.db import models

from core.models import AbstractBaseModel

__all__ = ("Comment",)


class Comment(AbstractBaseModel):
    """Represent comments."""

    text = models.TextField(help_text="Your comment")
    post = models.ForeignKey(
        "blog.Post",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The post this comment belongs to.",
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The author of this comment.",
    )

    def __str__(self):
        return f"{self.user} leave a comment on {self.post}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
