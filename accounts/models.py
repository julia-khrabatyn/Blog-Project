from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import AbstractBaseModel
from accounts.validators import validate_birth_day
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser, AbstractBaseModel):
    """Represent user"""

    birth_date = models.DateField(validators=[validate_birth_day])
    country = models.CharField(max_length=2)  # Country Code
    bio = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    @property
    def published_posts(self):
        """Get all user's published posts."""
        return self.posts.filter(published=True)

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]


class Follow(AbstractBaseModel):
    """Represent user's followers and user's followings."""

    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

    def clean(self):
        if self.follower == self.following:
            raise ValidationError("You can not follow yourself!")

    def __str__(self):
        return f"{self.follower} follows {self.following}"

    class Meta:
        unique_together = [("follower", "following")]
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
        indexes = [
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
        ]
