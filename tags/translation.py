from modeltranslation.translator import register, TranslationOptions
from .models import Tag


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ("title",)
    required_languages = ("en",)
