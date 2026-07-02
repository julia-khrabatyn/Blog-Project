from django import forms
from django.utils.translation import gettext_lazy as _

from ckeditor.widgets import CKEditorWidget
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import User

__all__ = [
    "AvatarUpdateForm",
    "UserProfileForm",
]

WIDGET_CLASS = "w-full p-2 border rounded-md focus:ring-sky-500"


class UserProfileForm(forms.ModelForm):
    """Form for extend/update user's personal info."""

    class Meta:
        model = User
        fields = ["birth_date", "country", "city", "bio"]
        labels = {
            "birth_date": _("Date of Birth"),
            "country": _("Country"),
            "city": _("City"),
            "bio": _("Bio"),
        }

    birth_date = forms.DateField(
        label=_("Date of Birth"),
        required=False,
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "class": WIDGET_CLASS,
            },
        ),
    )

    country = country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={"class": WIDGET_CLASS})
    )

    city = forms.CharField(
        label=_("City"),
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": WIDGET_CLASS,
                "placeholder": _("Enter your city"),
            }
        ),
    )

    bio = forms.CharField(
        label=_("Bio"),
        required=False,
        widget=CKEditorWidget(
            attrs={
                "class": WIDGET_CLASS,
            }
        ),
    )


class AvatarUpdateForm(forms.ModelForm):
    """Form for updating user's avatar (profile photo)."""

    class Meta:
        model = User
        fields = ("avatar",)
