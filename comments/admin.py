from django.contrib import admin

from core.admin import ExportCsvMixin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin, ExportCsvMixin):
    """Register Comment model in django-admin."""

    list_display = ("user", "post", "text")
    ordering = ["-updated_at"]
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("user", "post", "updated_at")
    fieldsets = (
        (
            "Who created",
            {
                "fields": ("user",),
            },
        ),
        ("To which post", {"fields": ("post",)}),
        (
            "Date of creation/updation",
            {"fields": ("created_at", "updated_at")},
        ),
        ("Comment text", {"fields": ("text",)}),
    )
    actions = ["export_as_csv"]
