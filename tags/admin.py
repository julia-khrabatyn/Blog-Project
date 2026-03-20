from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Register Tag model in django-admin."""

    list_display = ("title", "slug", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
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
