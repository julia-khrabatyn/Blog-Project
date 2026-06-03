from django.utils.translation import gettext_lazy as _

CONSTANCE_ADDITIONAL_FIELDS = {
    "image_field": ["django.forms.ImageField", {}],
}

CONSTANCE_CONFIG = {
    "MAX_IMAGE_SIZE_MB": (5, _("Max image size in MB"), int),
    "ALLOWED_IMAGE_TYPES": (
        "image/jpeg,image/webp,image/png",
        _("Allowed mime-type for image files"),
        str,
    ),
    "ALLOWED_IMAGE_EXTENSIONS": (
        "webp,png,jpeg,jpg",
        _("Allowed images extensions (comma-separated)"),
        str,
    ),
    "AVATAR_HEIGHT": (50, _("Avatar height in px"), int),
    "USER_ACTIVITY_LOW_LIMIT": (
        5,
        _("Threshold for low user's activity (number of likes)"),
        int,
    ),
    "USER_ACTIVITY_MEDIUM_LIMIT": (
        15,
        _("Threshold for medium user's activity (number of likes)"),
        int,
    ),
    "PAGINATE_BY": (3, _("number of posts showing in one page"), int),
    "COMMENTS_PAGINATION": (5, _("number of showing below post"), int),
    "DEFAULT_AVATAR": (
        "images/default_avatar.jpeg",
        _("Upload default user avatar"),
        "image_field",
    ),
    "MAP_GEO_OFFSET": (
        0.05,
        _("user's location offset for representation on map"),
        float,
    ),
}
