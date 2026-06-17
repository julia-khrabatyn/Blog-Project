import logging
import textwrap
import time

from deep_translator import GoogleTranslator

from config.settings.base_settings import LANGUAGES

LANGUAGES_LIST = [lang[0] for lang in LANGUAGES]


logger = logging.getLogger("core")

__all__ = [
    "get_changed_fields",
    "get_target_languages",
    "LANGUAGES_LIST",
    "translate_changed_fields",
]


def _get_lang_from_field(field_name: str) -> str:
    """Return source language from changed field by it's end."""
    return field_name.rsplit("_", 1)[-1]


def get_target_languages(source_lang: str) -> list[str]:
    """Function for generating languages for translation."""
    return [lang for lang in LANGUAGES_LIST if lang != source_lang]


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
        for i, chunk in enumerate(chunks):
            if i > 0:
                time.sleep(1)
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


def get_changed_fields(instance, fields: list, source_lang: str):
    """Protected function for checking if any field (that should be translated) was changed in DB."""
    if not instance.pk:
        return fields

    try:
        old_version = instance.__class__.objects.get(pk=instance.pk)

        changed = []

        for field in fields:
            field_name = f"{field}_{source_lang}"

            if getattr(old_version, field_name) != getattr(
                instance, field_name
            ):
                changed.append(field)

        return changed

    except instance.__class__.DoesNotExist:
        return fields


def translate_changed_fields(
    instance,
    changed_fields: list[str],
) -> None:

    for source_field in changed_fields:

        if "_" not in source_field:
            continue

        field_name, source_lang = source_field.rsplit("_", 1)

        target_langs = get_target_languages(source_lang)

        value = getattr(instance, source_field)
        if not value:
            continue

        for target_lang in target_langs:
            try:
                setattr(
                    instance,
                    f"{field_name}_{target_lang}",
                    _translate_text(
                        value,
                        source_lang=source_lang,
                        target_lang=target_lang,
                    ),
                )
            except Exception as e:
                logger.exception(f"Error {e} was occurred!", exc_info=True)
