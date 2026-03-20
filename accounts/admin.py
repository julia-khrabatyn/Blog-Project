from django.contrib import admin
from django.utils.safestring import mark_safe

from core.admin import ExportCsvMixin

from accounts.models import User, Follow

admin.site.site_header = "Byline Administration"
admin.site.site_title = "Your Byline Blog Admin Portal"
admin.site.index_title = "Welcome Back!"


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = "follower"
    extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    """Register User in django admin."""

    def show_avatar(self, obj):
        """Represent user's avatar in admin."""
        if obj.avatar:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=obj.avatar.url,
                    width=obj.avatar.width,
                    height=obj.avatar.height,
                )
            )
        else:
            return "No avatar"

    list_display = (
        "username",
        "email",
        "avatar",
        "show_avatar",
        "birth_date",
        "country",
        "city",
        "bio",
    )
    ordering = ["username"]
    list_filter = ("username", "country", "birth_date", "email", "updated_at")
    search_fields = ("username", "email")
    readonly_fields = ("created_at", "updated_at", "show_avatar")
    list_display_links = ("username", "email")
    fieldsets = (
        (
            "General User's info",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "date_joined",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "User's status info",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                ),
                "classes": ("collapse",),
                "description": ("Sensitive User's info"),
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "avatar",
                    "show_avatar",
                    "bio",
                ),
                "classes": ("collapse",),
                "description": ("Information about user"),
            },
        ),
        (
            "Location details",
            {
                "fields": ("country", "city"),
                "classes": ("collapse",),
                "description": ("User's location"),
            },
        ),
        (
            "User's Tags",
            {"fields": ("tags",), "classes": ("collapse",)},
        ),
    )
    date_hierarchy = "birth_date"
    actions_on_bottom = True
    list_per_page = 50
    inlines = [FollowInline]
    actions = ["export_as_csv"]
