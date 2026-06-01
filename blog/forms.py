from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from ckeditor.widgets import CKEditorWidget

from .models import Post

__all__ = [
    "PostForm",
]

WIDGET_CLASS = "w-full p-2 border rounded-md focus:ring-sky-500"


class PostForm(ModelForm):
    """Form for creating post."""

    title = forms.CharField(
        label=_("Post Title"),
        max_length=255,
        widget=forms.widgets.TextInput(
            attrs={
                "class": WIDGET_CLASS,
                "placeholder": _("Enter a catchy title..."),
            }
        ),
    )
    text = forms.CharField(
        widget=CKEditorWidget(),
        label=_("Post content"),
    )
    description = forms.CharField(
        label=_("Post description (optional)"),
        required=False,
        max_length=255,
        widget=forms.widgets.Textarea(
            attrs={
                "class": WIDGET_CLASS,
                "rows": 2,
                "placeholder": _("Short summary for the card..."),
            }
        ),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "description",
            "text",
            "categories",
            "tags",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["categories"].widget.attrs.update({"class": WIDGET_CLASS})
        self.fields["categories"].required = False
        category_text = _("Don't have the one you need?")
        category_link = _("+ Create Category")
        self.fields["categories"].help_text = mark_safe(
            f"{category_text} <a href='categories/create/' target='_blank' class='text-sky-500 hover:underline'>{category_link}</a>"
        )

        self.fields["tags"].widget.attrs.update({"class": WIDGET_CLASS})
        self.fields["tags"].required = False
        tag_text = _("Don't have the one you need?")
        tag_link = _("+ Add New Tag")
        self.fields["tags"].help_text = mark_safe(
            f"{tag_text}<a href='tags/create/' target='_blank' class='text-sky-500 hover:underline'>{tag_link}</a>"
        )

        def save(self, commit=True, user=None):
            post = super().save(commit=False)
            if user:
                post.user = user

            if commit:
                post.save()
                self.save_m2m()

            return post
