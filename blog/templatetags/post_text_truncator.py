from django import template
from django.utils.html import strip_tags
from django.utils.text import Truncator

register = template.Library()


def truncate_html_text(text: str, words_count: int = 50) -> str:
    """Truncate post text by default to 50 words, exclude html tags (from CKEditor)."""
    return Truncator(strip_tags(text)).words(words_count)


@register.filter
def preview(text, words=50):
    return truncate_html_text(text, words)
