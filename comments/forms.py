from django import forms
from django.forms import ModelForm

from django.utils.translation import gettext_lazy as _

from .models import Comment

WIDGET_CLASS = "w-full p-2 border rounded-md focus:ring-sky-500"

__all__ = ["CommentForm"]


class CommentForm(ModelForm):
    """Form for creating comments."""

    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": WIDGET_CLASS,
                    "rows": 4,
                    "placeholder": _("Add Your comment here:"),
                }
            )
        }
        labels = {"text": _("Comment text")}
