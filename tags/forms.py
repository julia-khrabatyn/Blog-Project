from django.utils.translation import gettext_lazy as _

from blog.forms import _BaseForm

from .models import Tag


class TagForm(_BaseForm):
    """ "Form for creating tag. (Include dynamic language switching.)"""

    title_label = _("Your tag title")
    title_placeholder = _("Enter tag title")

    class Meta:
        model = Tag
        fields = ["title_en", "title_uk"]
