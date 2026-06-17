from django.utils.translation import gettext_lazy as _

POST_FIELD_UI = {
    "title": {
        "label": _("Post Title"),
        "placeholder": _("Enter a catchy title..."),
    },
    "description": {
        "label": _("Post description (optional)"),
        "placeholder": _("Short summary for the card..."),
    },
    "text": {
        "label": _("Post content"),
        "placeholder": _("Share Your ideas with us!"),
    },
}

CATEGORY_FIELD_UI = {
    "title": {
        "label": _("Your category title"),
        "placeholder": _("Enter category title"),
    }
}
