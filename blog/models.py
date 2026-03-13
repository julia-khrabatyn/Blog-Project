from django.db import models
from core.models import AbstractBaseModel, PublishMixin
from accounts.models import User
from django.utils.functional import cached_property
from django.core.validators import FileExtensionValidator
from blog.validators import validate_image_file


# Create your models here.
class Post(AbstractBaseModel, PublishMixin):
    """Represent blog Post."""

    title = models.CharField(max_length=255)
    text = models.TextField()
    description = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    slug = models.SlugField(max_length=255, unique=True)
    categories = models.ManyToManyField(
        "Category", related_name="posts", blank=True
    )
    tags = models.ManyToManyField("tags.Tag", related_name="posts", blank=True)

    def __str__(self):
        return self.title.title()

    @property
    def short_text(self):
        """
        Get slice from post text for representing.
        """
        return self.text[:100]

    @cached_property
    def like_count(self):
        """Get all post's likes"""
        return self.likes.count()

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
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="images"
    )
    alt_text = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.alt_text.title() if self.alt_text else str(self.image_file)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        indexes = [models.Index(fields=["post"])]


class Like(AbstractBaseModel):
    """Represents user preferences for a specific post."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes"
    )

    def __str__(self):
        return f"{self.user} likes {self.post.title.title()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"], name="unique_like"
            )
        ]
        verbose_name = "Like"
        verbose_name_plural = "Likes"


class Category(AbstractBaseModel):
    """Represent a post category/categories."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

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
            models.Index(fields=["slug"]),
        ]
