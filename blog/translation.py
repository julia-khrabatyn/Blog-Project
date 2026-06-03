from modeltranslation.translator import register, TranslationOptions
from .models import Category, Post


@register(Category)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Post)
class ArticleTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "text",
        "description",
    )
