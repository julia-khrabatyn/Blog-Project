from django import template
from django.conf import settings
from django.templatetags.static import static

from constance import config

register = template.Library()

__all__ = [
    "get_user_avatar",
]


@register.simple_tag
def get_user_avatar(user_obj):
    """Function for getting user's avatar and return it for displaying it in templates."""

    # extract user's avatar if user upload it by himself.
    if hasattr(user_obj, "avatar") and user_obj.avatar:
        return user_obj.avatar.url

    # if user didn't upload avatar, but logged in using Google social account and have profile avatar in it -> get it.

    social = user_obj.socialaccount_set.filter(provider="google").first()
    if social:
        google_url = social.extra_data.get("picture")
        if google_url:
            return google_url

    # if neither user's avatar, nor google avatar -> then give to user default byline avatar.
    default_path = config.DEFAULT_AVATAR
    if default_path.startswith("images/"):
        return static(default_path)

    return f"{settings.MEDIA_URL}{default_path}"
