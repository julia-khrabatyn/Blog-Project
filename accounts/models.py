from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.db.models import F, Q

from django_countries.fields import CountryField

from core.models import AbstractBaseModel

from accounts.validators import validate_birth_date


class User(AbstractUser, AbstractBaseModel):
    """Represent user"""

    birth_date = models.DateField(validators=[validate_birth_date])
    country = (
        CountryField()
    )  # stores the 2-letter ISO 3166-1 country code. have autocomplete in admin
    bio = models.TextField(
        null=True, blank=True, validators=[MaxLengthValidator(500)]
    )
    city = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    tags = models.ManyToManyField("tags.Tag", blank=True, related_name="users")

    @property
    def published_posts(self):
        """Get all user's published posts."""
        return self.posts.filter(published=True)

    @property
    def liked_posts(self):
        """Get all posts, that user liked."""
        return self.likes.all()

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
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"], name="unique_follow"
            ),
            models.Constraint(
                check=~Q(follower=F("following")), name="prevent_self_follow"
            ),
        ]
        unique_together = [("follower", "following")]
        verbose_name = "Follow"
        verbose_name_plural = "Follows"
