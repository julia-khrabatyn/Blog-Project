from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext_lazy as _


from core.services.forms_services import BaseTranslationForm

from .models import Tag

WIDGET_CLASS = "w-full p-2 border rounded-md focus:ring-sky-500"

TAG_FIELD_UI = {
    "title": {
        "label": _("Your tag title"),
        "placeholder": _("Enter tag title"),
    }
}


class TagForm(BaseTranslationForm):
    """Form for creating tag. (Include dynamic language switching.)"""

    translatable_fields = ["title"]
    UI = TAG_FIELD_UI

    class Meta:
        model = Tag
        fields = ["title_en", "title_uk"]
        widgets = {"title": forms.TextInput(attrs={"class": WIDGET_CLASS})}
