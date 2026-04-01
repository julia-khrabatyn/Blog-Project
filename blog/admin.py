from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

from adminsortable2.admin import SortableAdminMixin
from constance import config

from core.admin import BaseExportCsvMixin

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
                    height=obj.image_file.height,
                    width=obj.image_file.width,
                )
            )
        else:
            return "No image."


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, BaseExportCsvMixin):
    """Register Post in django admin."""

    def get_queryset(self, request):
        """Handle lazy query -> boost productivity."""
        return (
            super()
            .get_queryset(request)
            .prefetch_related("tags", "categories")
            .select_related("user")
            .annotate(likes_count=Count("likes"))
        )

    @admin.display(description="Tags")
    def get_tags(self, obj):
        """Get tags for displaing it in admin."""
        return ", ".join([tag.title for tag in obj.tags.all()])

    @admin.display(description="Category")
    def get_category(self, obj):
        """Get category for displaing it in admin."""
        return ", ".join([category.title for category in obj.categories.all()])

    @admin.display(description="Likes", ordering="likes_count")
    def get_likes_count(self, obj):
        """Get total likes for post."""
        return obj.likes_count

    @admin.display(description="First 10 words from post text")
    def partial_post_text(self, obj):
        """Show first 10 words of post text."""
        return Truncator(obj.text).words(10, truncate="...")

    @admin.display(description="First 5 tags for post")
    def partial_post_tags(self, obj):
        """Display first 5 tags of all possible post tags."""
        tags_list = [tag.title for tag in obj.tags.all()]
        if not tags_list:
            return "❌"
        return ", ".join(tags_list[:5]) + ("..." if len(tags_list) > 5 else "")

    list_display = (
        "user",
        "title",
        "get_likes_count",
        "description",
        "get_category",
        "partial_post_tags",
        "partial_post_text",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    list_filter = (
        "title",
        "user",
        "categories",
        "tags",
    )
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
    filter_horizontal = ("tags",)  # add opportunity to choose many tags
    actions_on_bottom = True
    list_per_page = 50
    actions = ["export_as_csv"]
    date_hierarchy = "updated_at"
    inlines = [ImageInLine]


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Register Category in django-admin."""

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(posts_count_db=Count("posts"))
        )

    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "posts_count_display")
    fieldsets = (
        (
            "Category info",
            {
                "fields": (
                    "title",
                    "slug",
                    "created_at",
                    "updated_at",
                    "posts_count_display",
                )
            },
        ),
    )
    list_display = ("order", "title", "posts_count_display", "updated_at")
    list_filter = ("title", "created_at", "updated_at")

    @admin.display(description="Number of posts", ordering="posts_count_db")
    def posts_count_display(self, obj):
        return obj.posts_count_db


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


class UserActivityFilter(admin.SimpleListFilter):
    """Help to display filter for likes."""

    title = "User activity"
    parameter_name = "activity_level"

    @property
    def low_limit(self):
        """Get value from django-constance for low activity."""
        return config.USER_ACTIVITY_LOW_LIMIT

    @property
    def medium_limit(self):
        """Get value from django-constance for medium activity."""
        return config.USER_ACTIVITY_MEDIUM_LIMIT

    def lookups(self, request, model_admin):
        return (
            ("low", f"Low (1-{self.low_limit} likes)"),
            ("medium", f"Medium ({self.low_limit+1}-{self.medium_limit})"),
            ("high", f"High ({self.medium_limit + 1}+ likes)"),
        )

    def queryset(self, request, queryset):
        value = self.value
        if value == "low":
            return queryset.filter(user_total_likes_count__lte=self.low_limit)
        if value == "medium":
            return queryset.filter(
                user_total_likes_count__gt=self.low_limit,
                user_total_likes_count__lte=self.medium_limit,
            )
        if self.value == "high":
            return queryset.filter(
                user_total_likes_count__gt=self.medium_limit
            )

        return queryset


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin, BaseExportCsvMixin):
    """Register Like model in django-admin."""

    list_display = ("user", "post", "user_total_likes", "updated_at")
    ordering = ["-updated_at"]
    list_filter = ("user", "post", "updated_at", UserActivityFilter)
    list_display_links = ("user", "post")
    actions = ["export_as_csv"]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user", "post")
            .annotate(user_total_likes_count=Count("user__likes"))
        )

    @admin.display(
        description="Total users likes",
        ordering="user_total_likes_count",
    )
    def user_total_likes(self, obj):
        """Count total user's likes."""
        return obj.user_total_likes_count
