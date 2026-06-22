from django.utils.html import strip_tags
from django.utils.text import Truncator


def truncate_html_text(text: str, words_count: int = 50) -> str:
    """Truncate post text by default to 50 words, exclude html tags (from CKEditor)."""
    return Truncator(strip_tags(text)).words(words_count)
