from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import BaseExportCsvMixin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin, BaseExportCsvMixin):
    """Register Comment model in django-admin."""

    list_display = ("user", "post", "text")
    ordering = ["-updated_at"]
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("user", "post", "updated_at")
    fieldsets = (
        (
            _("Who created"),
            {
                "fields": ("user",),
            },
        ),
        (
            _("To which post"),
            {
                "fields": ("post",),
            },
        ),
        (
            _("Date of creation/update"),
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
        (
            _("Comment text"),
            {
                "fields": ("text",),
            },
        ),
    )
    actions = ["export_as_csv"]
