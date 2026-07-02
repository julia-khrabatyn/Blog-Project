from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .models import User

__all__ = [
    "UserOwnerMixin",
]


class UserOwnerMixin(UserPassesTestMixin):
    """Allow access only to the owner profile."""

    slug_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        self.target_user = get_object_or_404(
            User, username=kwargs[self.slug_url_kwarg]
        )
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.kwargs[self.slug_url_kwarg] == self.request.user.username
        )
