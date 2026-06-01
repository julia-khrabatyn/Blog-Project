from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractBaseModel

__all__ = ("Comment",)


class Comment(AbstractBaseModel):
    """Represent comments."""

    text = models.TextField(
        verbose_name=_("Text"), help_text=_("Your comment")
    )
    post = models.ForeignKey(
        "blog.Post",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Post"),
        help_text=_("The post this comment belongs to."),
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("User"),
        help_text=_("The author of this comment."),
    )

    def __str__(self):
        return f"{self.user} left a comment on {self.post}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
