from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TabbedTranslationAdmin

from tags.models import Tag

__all__ = ["TagAdmin"]


@admin.register(Tag)
class TagAdmin(TabbedTranslationAdmin):
    """Register Tag model in django-admin."""

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        lang = request.LANGUAGE_CODE

        # inactivate non-required lang

        if lang == "uk":
            if "title_en" in form.base_fields:
                form.base_fields["title_en"].required = False
        else:
            if "title_uk" in form.base_fields:
                form.base_fields["title_uk"].required = False

        return form

    list_display = ("title", "slug", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title_en",)}
    list_filter = (
        "title",
        "updated_at",
    )
    fieldsets = (
        (
            _("Tags info"),
            {
                "fields": ("title", "slug", "created_at", "updated_at"),
            },
        ),
    )
