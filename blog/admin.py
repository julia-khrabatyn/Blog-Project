from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from blog.models import Category, Image, Like, Post


@admin.register(Post)
class Post(SortableAdminMixin, admin.ModelAdmin):
    """Register Post in django admin."""

    @admin.display(description="Tags")
    def get_tags(self, obj):
        """Get tags for displaing it in admin."""
        return ", ".join([tag.title for tag in obj.tags.all()])

    @admin.display(description="Category")
    def get_category(self, obj):
        """Get category for displaing it in admin."""
        return ", ".join([category.title for category in obj.categories.all()])

    list_display = (
        "user",
        "title",
        "description",
        "get_category",
        "get_tags",
        "text",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("title", "user", "categories", "tags")
    ordering = ["-updated_at"]
    fieldsets = (
        (
            "Post info",
            {
                "fields": (
                    "user",
                    "categories",
                    "tags",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Post details",
            {
                "fields": ("title", "slug", "text", "description"),
                "classes": ("collapse",),
            },
        ),
    )
