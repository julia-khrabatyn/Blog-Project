from django import template
from django.conf import settings
from django.urls import resolve, reverse

register = template.Library()

__all__ = ["language_switcher"]


@register.inclusion_tag("includes/_language_switcher.html", takes_context=True)
def language_switcher(context):
    request = context.get("request")

    next_url = request.get_full_path()

    for code, _ in settings.LANGUAGES:
        if next_url.startswith(f"/{code}/"):
            next_url = "/" + next_url[len(f"/{code}/") :]
            break
        elif next_url == f"/{code}":
            next_url = "/"
            break

    return {
        "next": next_url,
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE"),
        "LANGUAGES": settings.LANGUAGES,
    }
