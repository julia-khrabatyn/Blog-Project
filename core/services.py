import logging
import textwrap

from deep_translator import GoogleTranslator
from .middleware import get_current_language

# TODO: should I add time module for time sleep between chunks, so error 429 Too Many Requests won't happen?
logger = logging.getLogger("core")

__all__ = ["translate_changed_fields", "get_translation_field_map"]


def _translate_text(text: str, source_lang, target_lang) -> str:
    """Protected function for translating text from en to uk."""
    if not text:
        return text
    try:
        # limit for google translation 5000 symbols
        if len(text) < 4000:
            return GoogleTranslator(
                source=source_lang, target=target_lang
            ).translate(text=text)
        chunks = textwrap.wrap(text=text, width=4000, replace_whitespace=False)
        translated_parts = []
        for chunk in chunks:
            translated_chunk = GoogleTranslator(
                source=source_lang, target=target_lang
            ).translate(text=chunk)
            translated_parts.append(translated_chunk)
        return " ".join(translated_parts)
    except ValueError as e:
        logger.exception(
            f"ValueError was occurred while running translation from {source_lang} to {target_lang} language!",
            exc_info=True,
        )
        return text
    except Exception as e:
        logger.exception(
            f"Error {e} was occurred while running translation from {source_lang} to {target_lang} language!",
            exc_info=True,
        )
        return text


def _get_changed_fields(instance, fields: list) -> list:
    """Protected function for checking if any field (that should be translated) was changed in DB."""
    if not instance.pk:
        return fields
    try:
        old_version = instance.__class__.objects.get(pk=instance.pk)
        return [
            f
            for f in fields
            if getattr(old_version, f) != getattr(instance, f)
        ]
    except instance.__class__.DoesNotExist:
        return fields


def translate_changed_fields(instance, fields_map: dict) -> None:
    """Main function for translation."""
    lang = get_current_language()
    source_lang, target_lang = ("en", "uk") if lang == "en" else ("uk", "en")
    changed = _get_changed_fields(instance, list(fields_map.keys()))
    logger.warning(f"fields_map: {fields_map}")
    logger.warning(f"changed: {changed}")
    for source_field, target_field in fields_map.items():
        if source_field in changed and getattr(instance, source_field):
            try:
                setattr(
                    instance,
                    target_field,
                    _translate_text(
                        getattr(instance, source_field),
                        source_lang=source_lang,
                        target_lang=target_lang,
                    ),
                )
            except Exception as e:
                logger.exception(f"Error {e} was occurred!", exc_info=True)


def get_translation_field_map(fields: list[str]) -> dict:
    """Returns fields map based on current user interface language."""
    lang = get_current_language()

    if lang == "uk":
        return {f"{field}_uk": f"{field}_en" for field in fields}
    return {f"{field}_en": f"{field}_uk" for field in fields}
