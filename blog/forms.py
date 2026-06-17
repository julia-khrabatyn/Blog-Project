from django import forms

from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.services.forms_services import BaseTranslationForm

from .models import Post, Category
from .forms_config import POST_FIELD_UI, CATEGORY_FIELD_UI

__all__ = [
    "PostForm",
    "PostAdminForm",
    "CategoryForm",
    "CategoryAdminForm",
]

WIDGET_CLASS = "w-full p-2 border rounded-md focus:ring-sky-500"


class PostForm(BaseTranslationForm):
    """Form for creating post. (Include dynamic language switching.)"""

    translatable_fields = ["title", "description", "text"]
    optional_fields = ["description", "categories", "tags"]
    UI = POST_FIELD_UI

    class Meta:
        model = Post
        fields = [
            "title_en",
            "title_uk",
            "description_en",
            "description_uk",
            "text_en",
            "text_uk",
            "categories",
            "tags",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": WIDGET_CLASS}),
            "description": forms.Textarea(
                attrs={"class": WIDGET_CLASS, "rows": 3}
            ),
            "text": CKEditorUploadingWidget(),
            "categories": forms.SelectMultiple(attrs={"class": WIDGET_CLASS}),
            "tags": forms.SelectMultiple(attrs={"class": WIDGET_CLASS}),
        }


class PostAdminForm(PostForm):
    """Form for admin — shows ALL language fields at once."""

    def _hide_non_current_language_fields(self):
        pass


class CategoryForm(BaseTranslationForm):
    """Form for creating category. (Include dynamic language switching.)"""

    translatable_fields = ["title"]
    UI = CATEGORY_FIELD_UI

    class Meta:
        model = Category
        fields = ["title_en", "title_uk"]
        widgets = {"title": forms.TextInput(attrs={"class": WIDGET_CLASS})}


class CategoryAdminForm(CategoryForm):
    """Form for admin — shows ALL language fields at once."""

    def _hide_non_current_language_fields(self):
        pass
