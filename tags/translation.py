from modeltranslation.translator import register, TranslationOptions
from .models import Tag


@register(Tag)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title",)
