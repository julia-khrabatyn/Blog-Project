from django.contrib import admin

from adminsortable2.admin import SortableAdminMixin

from accounts.models import User, Follow

admin.site.site_header = "Byline Administration"
admin.site.site_title = "Your Byline Blog Admin Portal"
admin.site.index_title = "Welcome Back!"


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = "follower"
    extra = 0


@admin.register(User)
class UserAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Register User in django admin."""

    list_display = (
        "username",
        "email",
        "avatar",
        "birth_date",
        "country",
        "city",
        "bio",
    )
    ordering = ["username"]
    list_filter = ("username", "country", "birth_date", "email")
    search_fields = ("username", "email")
    readonly_fields = ("created_at", "updated_at")
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
