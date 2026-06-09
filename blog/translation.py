from modeltranslation.translator import register, TranslationOptions
from .models import Category, Post


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "text",
        "description",
    )
