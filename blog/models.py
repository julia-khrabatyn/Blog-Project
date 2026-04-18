from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from accounts.models import User
from core.models import AbstractBaseModel, PublishMixin, SlugMixin


from blog.validators import validate_image_file, validate_image_extension

__all__ = ("Category", "Image", "Like", "Post")


class Post(AbstractBaseModel, PublishMixin, SlugMixin):
    """Represent blog Post."""

    title = models.CharField(
        max_length=255, help_text="Your post title", unique=True
    )
    text = RichTextUploadingField(help_text="Post text")
    description = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Post description (optional)",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        help_text="User, created post",
    )
    categories = models.ManyToManyField(
        "Category",
        related_name="posts",
        blank=True,
        help_text="Post category (optional)",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        related_name="posts",
        blank=True,
        help_text="your post tag (optional)",
    )

    def __str__(self):
        return self.title.title()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Post"
        verbose_name_plural = "Posts"
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
        help_text="Upload your image (allowed formats: .png, .jpeg, .jpg, .webp files; max file size: 5 MB)",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="This image belongs to (post)",
    )
    alt_text = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Alternative image text",
    )

    def __str__(self):
        return self.alt_text.title() if self.alt_text else str(self.image_file)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class Like(AbstractBaseModel):
    """Represents user preferences for a specific post."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes",
        help_text="Like from user",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        help_text="like to post",
    )

    def __str__(self):
        return f"{self.user} likes {self.post}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_like"
            )
        ]
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        indexes = [
            models.Index(fields=["user", "post"]),
        ]


class Category(AbstractBaseModel, SlugMixin):
    """Represent a post category/categories."""

    title = models.CharField(max_length=255, help_text="Your category title")
    order = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.title.title()

    class Meta:
        ordering = ["order"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["title"]),
        ]
