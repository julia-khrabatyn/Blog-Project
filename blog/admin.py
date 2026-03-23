from django.contrib import admin
from django.utils.safestring import mark_safe

from adminsortable2.admin import SortableAdminMixin

from core.admin import ExportCsvMixin

from blog.models import Category, Image, Like, Post


class ImageInLine(admin.TabularInline):
    """class for representing all images added to post."""

    model = Image
    extra = 0
    readonly_fields = ("show_image",)

    def show_image(self, obj):
        if obj.image_file:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=obj.image_file.url,
                    width=obj.image_file.width,
                    height=obj.image_file.height,
                )
            )
        else:
            return "No image."


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, ExportCsvMixin):
    """Register Post in django admin."""

    def get_queryset(self, request):
        """Handle lazy query -> boost productivity."""
        return (
            super()
            .get_queryset(request)
            .prefetch_related("tags", "categories")
            .select_related("user")
        )

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
    actions_on_bottom = True
    list_per_page = 50
    actions = ["export_as_csv"]
    date_hierarchy = "updated_at"
    inlines = [ImageInLine]


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Register Category in django-admin."""

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("posts")

    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            "Category info",
            {"fields": ("title", "slug", "created_at", "updated_at")},
        ),
    )
    list_filter = ("title", "created_at", "updated_at")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Register Image in django-admin"""

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("post")

    def show_image(self, obj):
        """Represent image in post."""
        if obj.image_file:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=obj.image_file.url,
                    width=obj.image_file.width,
                    height=obj.image_file.height,
                )
            )
        else:
            return "Image not added yet."

    list_display = (
        "image_file",
        "alt_text",
        "post",
        "show_image",
        "created_at",
        "updated_at",
    )
    ordering = ["updated_at"]
    readonly_fields = ("created_at", "updated_at", "show_image")
    list_filter = ("created_at", "updated_at", "alt_text", "post")
    fieldsets = (
        (
            "Post's image general info",
            {
                "fields": (
                    "image_file",
                    "show_image",
                    "alt_text",
                    "post",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Image creation/updation time",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Register Like model in django-admin."""

    list_display = ("user", "post", "updated_at")
    ordering = ["-updated_at"]
    list_filter = ("user", "post", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "post")
