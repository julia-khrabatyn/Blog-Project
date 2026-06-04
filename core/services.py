import logging
import textwrap
from deep_translator import GoogleTranslator

# TODO: should I add time module for time sleep between chunks, so error 429 Too Many Requests won't happen?
logger = logging.getLogger("core")

__all__ = ["translate_changed_fields"]


def _translate_text(text: str, source_lang="en", target_lang="uk") -> str:
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
            f"ValueError was occurred while running translation from {source_lang} to {target_lang} language!"
        )
        return text
    except Exception as e:
        logger.exception(
            f"Error {e} was occurred while running translation from {source_lang} to {target_lang} language!"
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
    changed = _get_changed_fields(instance, list(fields_map.keys()))
    for en_field, uk_field in fields_map.items():
        if en_field in changed and getattr(instance, en_field):
            try:
                setattr(
                    instance,
                    uk_field,
                    _translate_text(getattr(instance, en_field)),
                )
            except Exception as e:
                logger.exception(f"Error {e} was occurred!")
