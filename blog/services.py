import folium
import random

from django.apps import apps
from django.contrib.staticfiles import finders
from django.core.paginator import Paginator
from django.db.models import Count

from constance import config
from folium.plugins import HeatMap
from pathlib import Path

from .filters import CommentFilter

Post = apps.get_model("blog", "Post")

ICON_PATH = finders.find("images/icon.png")

__all__ = [
    "generate_users_heatmap",
    "generate_single_user_map",
    "get_comments_for_post_view",
    "get_filtered_posts",
]


def generate_users_heatmap(users_queryset):
    """Function for generating heatmap out of user's geodata using folium."""
    m = folium.Map(
        location=[48.3794, 31.1656], zoom_start=5, tiles="CartoDB positron"
    )
    heat_data = []
    map_offset = config.MAP_GEO_OFFSET
    for user in users_queryset:
        if user.latitude is not None and user.longitude is not None:
            # add little noise to user's coords
            latitude = float(user.latitude) + random.uniform(
                -map_offset, map_offset
            )
            longitude = float(user.longitude) + random.uniform(
                -map_offset, map_offset
            )
            coords = [latitude, longitude]
            heat_data.append(coords)
            folium.Marker(
                location=coords,
                popup=f"{user.username}, ({user.city or user.country})",
                icon=folium.Icon(icon="user", color="blue"),
            ).add_to(m)
    if heat_data:
        HeatMap(heat_data, radius=15).add_to(m)
    return m._repr_html_()


def _get_marker_icon() -> folium.Icon | folium.CustomIcon:
    """Function for getting folium.CustomIcon if provided valid custom image or getting  default folium.Icon."""
    if ICON_PATH and Path(ICON_PATH).is_file():
        # TODO: should I cover it in try: ... except... statement? or just leave it that way?
        return folium.CustomIcon(
            ICON_PATH,
            icon_size=(60, 70),
            icon_anchor=(20, 40),
            popup_anchor=(0, -40),
        )
    return folium.Icon(color="blue")


def generate_single_user_map(user):
    """Function for generating map out of user geodata (if provided) using folium."""
    if not user.latitude or not user.longitude:
        return None

    coords = [user.latitude, user.longitude]
    m = folium.Map(location=coords, zoom_start=7, tiles="CartoDB positron")

    folium.Marker(
        location=coords,
        popup=f"Author: {user.username}",
        icon=_get_marker_icon(),
    ).add_to(m)
    return m._repr_html_()


def _sort_comments(queryset, sort_method):
    """Private function for valid sorting comments."""

    valid_sorts = [
        "created_at",
        "-created_at",
    ]
    if sort_method in valid_sorts:
        return queryset.order_by(sort_method)
    return queryset


def _paginate_queryset(queryset, page_number, items_per_page):
    """Private function for comments pagination."""

    paginator = Paginator(queryset, items_per_page)
    return paginator.get_page(page_number)


def get_comments_for_post_view(post, query_params, items_per_page):
    """Function for getting filtered, sorted and paginated comments for specific post."""

    comments = post.comments.select_related("user").all()

    comment_filter = CommentFilter(query_params, queryset=comments)

    sort_method = query_params.get("sort", "-created_at")
    sorted_comments = _sort_comments(comment_filter.qs, sort_method)

    page_num = query_params.get("page")
    page_obj = _paginate_queryset(sorted_comments, page_num, items_per_page)

    return page_obj, comment_filter


def get_filtered_posts(query_params, filter_class, queryset=None):
    """Function for posts filtering."""

    if queryset is None:
        queryset = (
            Post.objects.filter(published=True)
            .select_related("user")
            .prefetch_related("categories")
        )

    queryset = queryset.annotate(likes_count=Count("likes"))
    post_filter = filter_class(query_params, queryset=queryset)

    return post_filter
