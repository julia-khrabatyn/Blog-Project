from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.models import User
from core.models import AbstractBaseModel, PublishMixin, SlugMixin

from blog.validators import validate_image_file


class Post(AbstractBaseModel, PublishMixin, SlugMixin):
    """Represent blog Post."""

    title = models.CharField(max_length=255, help_text="Your post title")
    text = models.TextField(help_text="Your post text")
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

    @property
    def short_text(self):
        """
        Get slice from post text for representing.
        """
        return self.text[:100]

    @property
    def like_count(self):
        """Get all post's likes"""
        return self.likes.count()

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
            FileExtensionValidator(
                allowed_extensions=["jpg", "png", "jpeg", "webp"]
            ),
            validate_image_file,
        ],
        help_text="Upload your image (use can use only .png, .jpeg, .jpg, .webp files)",
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


class Category(AbstractBaseModel, SlugMixin):
    """Represent a post category/categories."""

    title = models.CharField(max_length=255, help_text="Your category title")

    @property
    def posts_count(self):
        """Count all posts in category."""
        return self.posts.count()

    def __str__(self):
        return self.title.title()

    class Meta:
        ordering = ["title"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["title"]),
        ]
