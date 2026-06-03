from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from tags.models import Tag

__all__ = ["TagAdmin"]


@admin.register(Tag)
class TagAdmin(TabbedTranslationAdmin):
    """Register Tag model in django-admin."""

    list_display = ("title", "slug", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title_en",)}
    list_filter = (
        "title",
        "updated_at",
    )
    fieldsets = (
        (
            "Tags info",
            {
                "fields": ("title", "slug", "created_at", "updated_at"),
            },
        ),
    )
