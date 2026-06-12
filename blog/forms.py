from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from core.services import get_languages

from .models import Post, Category

__all__ = [
    "PostForm",
    "CategoryForm",
]

WIDGET_CLASS = "w-full p-2 border rounded-md focus:ring-sky-500"


class PostForm(ModelForm):
    """Form for creating post. (Include dynamic language switching.)"""

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lang, other_lang = get_languages()

        self.fields[f"title_{lang}"].required = True
        self.fields[f"title_{lang}"].label = _("Post Title")
        self.fields[f"title_{lang}"].widget = forms.widgets.TextInput(
            attrs={
                "class": WIDGET_CLASS,
                "placeholder": _("Enter a catchy title..."),
            }
        )

        self.fields[f"description_{lang}"].required = False
        self.fields[f"description_{lang}"].label = _(
            "Post description (optional)"
        )
        self.fields[f"description_{lang}"].widget = forms.widgets.Textarea(
            attrs={
                "class": WIDGET_CLASS,
                "rows": 2,
                "placeholder": _("Short summary for the card..."),
            }
        )

        self.fields[f"text_{lang}"].required = True
        self.fields[f"text_{lang}"].label = _("Post content")
        self.fields[f"text_{lang}"].widget = CKEditorUploadingWidget()

        for field in (
            f"title_{other_lang}",
            f"description_{other_lang}",
            f"text_{other_lang}",
        ):
            self.fields[field].required = False
            self.fields[field].widget = forms.HiddenInput()

        self.fields["categories"].required = False
        self.fields["categories"].widget.attrs.update({"class": WIDGET_CLASS})
        category_text = _("Don't have the one you need?")
        category_link = _("+ Create Category")
        self.fields["categories"].help_text = mark_safe(f"""
        {category_text}
        <button
            type="button"
            id="open-category-modal"
            class="text-sky-500 hover:underline"
        >
            {category_link}
        </button>
        """)

        self.fields["tags"].widget.attrs.update({"class": WIDGET_CLASS})
        self.fields["tags"].required = False
        tag_text = _("Don't have the one you need?")
        tag_link = _("+ Add New Tag")
        self.fields["tags"].help_text = mark_safe(
            f"{tag_text} <a href='#' target='_blank' class='text-sky-500 hover:underline'>{tag_link}</a>"
        )


class CategoryForm(ModelForm):
    """Form for creating category. (Include dynamic language switching.)"""

    class Meta:
        model = Category
        fields = [
            "title_en",
            "title_uk",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        lang, other_lang = get_languages()
        self.fields[f"title_{lang}"].required = True
        self.fields[f"title_{lang}"].label = _("Your category title")
        self.fields[f"title_{lang}"].widget = forms.widgets.TextInput(
            attrs={
                "class": WIDGET_CLASS,
                "placeholder": _("Enter category title..."),
            }
        )

        self.fields[f"title_{other_lang}"].required = False
        self.fields[f"title_{other_lang}"].widget = forms.HiddenInput()
