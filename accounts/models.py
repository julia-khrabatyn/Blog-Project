from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models

from ckeditor.fields import RichTextField
from django_countries.fields import CountryField

from core.models import AbstractBaseModel

from accounts.validators import validate_birth_date

__all__ = ("CustomUserManager", "Follow", "User")


class CustomUserManager(BaseUserManager):
    """Custom Manager for User model"""

    def create_user(
        self, username=None, email=None, password=None, **extra_fields
    ):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")

        if username is None:
            username = email.split("@")[0]

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser, AbstractBaseModel):
    """Represent user"""

    REQUIRED_FIELDS = ["email"]
    birth_date = models.DateField(
        # validators=[validate_birth_date],
        help_text="Your date of birth. Must be 13+ years for registartion",
        blank=True,
        null=True,
    )
    country = CountryField(
        help_text="Your country code", blank=True, null=True
    )
    # stores the 2-letter ISO 3166-1 country code. have autocomplete in admin
    bio = RichTextField(
        max_length=500, blank=True, null=True, config_name="special"
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Your city (optional)",
    )
    email = models.EmailField(
        unique=True, help_text="Your valid email address"
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        null=True,
        blank=True,
        help_text="Upload profile photo (optional) (Support only .png, .jpeg, .jpg, .webp extensions)",
    )
    tags = models.ManyToManyField(
        "tags.Tag",
        blank=True,
        related_name="users",
        help_text="Add tag (optional)",
    )
    objects = CustomUserManager()

    @property
    def published_posts(self):
        """Get all user's published posts."""
        return self.posts.filter(published=True)

    @property
    def liked_posts(self):
        """Get all posts, that user liked."""
        return self.likes.all()

    def __str__(self):
        full_name = f"{self.first_name or ""} {self.last_name or ""}".strip()
        if full_name:
            return full_name
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]


class Follow(AbstractBaseModel):
    """Represent user's followers and user's followings."""

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        help_text="User, who follows",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        help_text="User, who are followed",
    )

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You can not follow yourself!")

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow"
            ),
            models.CheckConstraint(
                condition=~models.Q(follower=models.F("following")),
                name="prevent_self_follow",
            ),
        ]
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
