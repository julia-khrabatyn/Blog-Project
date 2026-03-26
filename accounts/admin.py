from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from constance import config

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
class UserAdmin(BaseUserAdmin, ExportCsvMixin):
    """Register User in django admin with custom fields."""

    @admin.display(description="Preview")
    def show_avatar(self, obj):
        """Represent user's avatar in admin."""
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" style="width:{config.AVATAR_HEIGHT}px; height:{config.AVATAR_HEIGHT}px; object-fit:cover;" />'
            )
        else:
            return "No avatar"

    @admin.display(description="Has avatar", boolean=True)
    def has_avatar(self, obj):
        """Display mark whether person has or hasn't avatar"""
        return bool(obj.avatar)

    list_display = (
        "username",
        "email",
        "show_avatar",
        "has_avatar",
        "birth_date",
        "country",
        "is_staff",
        "is_active",
        "city",
        "bio",
    )
    ordering = ["username"]
    list_filter = ("username", "country", "birth_date", "email", "updated_at")
    search_fields = ("username", "email")
    readonly_fields = (
        "created_at",
        "updated_at",
        "show_avatar",
        "date_joined",
    )
    list_display_links = ("username", "email")
    fieldsets = (
        (
            "Credentials",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "User's personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "avatar",
                    "show_avatar",
                    "bio",
                    "tags",
                ),
                "classes": ("collapse",),
                "description": ("User's profile info"),
            },
        ),
        (
            "Permissions and status info",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
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
            "Important dates",
            {
                "fields": ("date_joined", "created_at", "updated_at"),
                "classes": ("collapsed",),
            },
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Extra Info",
            {
                "fields": ("email", "birth_date", "country", "city"),
            },
        ),
    )
    date_hierarchy = "birth_date"
    actions_on_bottom = True
    list_per_page = 50
    inlines = [FollowInline]
    actions = ["export_as_csv"]
