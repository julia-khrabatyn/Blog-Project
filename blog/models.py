from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField

from core.models import AbstractBaseModel, PublishMixin, SlugMixin


from blog.validators import validate_image_file, validate_image_extension

__all__ = ("Category", "Image", "Like", "Post")

User = get_user_model()


class Post(AbstractBaseModel, PublishMixin, SlugMixin):
    """Represent blog Post."""

    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Your post title"),
        unique=True,
    )
    text = RichTextUploadingField(
        help_text=_("Post text"), verbose_name=_("Text")
    )
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Post description (optional)"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Author"),
        help_text=_("User, created post"),
    )
    categories = models.ManyToManyField(
        "Category",
        related_name="posts",
        blank=True,
        verbose_name=_("Categories"),
        help_text=_("Post category (optional)"),
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        related_name="posts",
        blank=True,
        verbose_name=_("Tags"),
        help_text=_("your post tag (optional)"),
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["user", "published"]),
            models.Index(fields=["user", "published", "created_at"]),
        ]


class Image(AbstractBaseModel):
    """Represent image object."""

    image_file = models.ImageField(
        upload_to="images/",
        validators=[
            validate_image_extension,
            validate_image_file,
        ],
        verbose_name=_("Image file"),
        help_text=_(
            "Upload your image (allowed formats: .png, .jpeg, .jpg, .webp files; max file size: 5 MB)"
        ),
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Post"),
        help_text=_("This image belongs to (post)"),
    )
    alt_text = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("Alternative text"),
        help_text=_("Alternative image text"),
    )

    def __str__(self):
        return self.alt_text.title() if self.alt_text else str(self.image_file)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class Like(AbstractBaseModel):
    """Represents user preferences for a specific post."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name=_("User"),
        help_text=_("User, who liked the post"),
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name=_("Post"),
        help_text=_("Post that was liked"),
    )

    def __str__(self):
        return f"{self.user} likes {self.post}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_like"
            )
        ]
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        indexes = [
            models.Index(fields=["user", "post"]),
        ]


class Category(AbstractBaseModel, SlugMixin):
    """Represent a post category/categories."""

    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Your category title"),
    )
    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name=_("Order"),
        help_text=_("Display order priority (ascending)"),
    )

    def __str__(self):
        return self.title.title()

    class Meta:
        ordering = ["order"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        indexes = [
            models.Index(fields=["title"]),
        ]
