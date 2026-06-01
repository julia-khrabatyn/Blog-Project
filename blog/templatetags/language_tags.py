from django import template
from django.conf import settings

register = template.Library()

__all__ = ["language_switcher"]


@register.inclusion_tag("includes/_language_switcher.html", takes_context=True)
def language_switcher(context):
    request = context.get("request")

    return {
        "request": request,
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE"),
        "LANGUAGES": context.get("LANGUAGES"),
    }
