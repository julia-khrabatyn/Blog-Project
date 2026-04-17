CONSTANCE_ADDITIONAL_FIELDS = {
    "image_field": ["django.forms.ImageField", {}],
}

CONSTANCE_CONFIG = {
    "MAX_IMAGE_SIZE_MB": (5, "Max image size in MB", int),
    "ALLOWED_IMAGE_TYPES": (
        "image/jpeg,image/webp,image/png",
        "Allowed mime-type for image files",
        str,
    ),
    "ALLOWED_IMAGE_EXTENSIONS": (
        "webp,png,jpeg,jpg",
        "Allowed images extensions (comma-separated)",
        str,
    ),
    "AVATAR_HEIGHT": (50, "Avatar height in px", int),
    "USER_ACTIVITY_LOW_LIMIT": (
        5,
        "Threshold for low user's activity (number of likes)",
        int,
    ),
    "USER_ACTIVITY_MEDIUM_LIMIT": (
        15,
        "Threshold for medium user's activity (number of likes)",
        int,
    ),
    "PAGINATE_BY": (3, "number of posts showing in one page", int),
    "DEFAULT_AVATAR": (
        "images/default_avatar.jpeg",
        "Upload default user avatar",
        "image_field",
    ),
}
