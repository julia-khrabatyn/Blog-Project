import folium
import random

from django.contrib.staticfiles import finders

from constance import config
from folium.plugins import HeatMap

ICON_PATH = finders.find("images/icon.png")

__all__ = [
    "generate_users_heatmap",
    "generate_singlr_user_map",
]


def generate_users_heatmap(users_queryset):
    """Function for generating heatmap out of user's geodata using folium."""
    m = folium.Map(
        location=[48.3794, 31.1656], zoom_start=5, tiles="CartoDB positron"
    )
    heat_data = []
    for user in users_queryset:
        if user.latitude is not None and user.longitude is not None:
            # add little noise to user's coords
            latitude = float(user.latitude) + random.uniform(
                -config.MAP_GEO_OFFSET, config.MAP_GEO_OFFSET
            )
            longitude = float(user.longitude) + random.uniform(
                -config.MAP_GEO_OFFSET, config.MAP_GEO_OFFSET
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


def generate_single_user_map(user):
    """Function for generating map out of user geodata (if provided) using folium."""
    if not user.latitude or not user.longitude:
        return None

    coords = [user.latitude, user.longitude]
    m = folium.Map(location=coords, zoom_start=7, tiles="CartoDB positron")
    custom_icon = folium.CustomIcon(
        ICON_PATH,
        icon_size=(60, 70),
        icon_anchor=(20, 40),
        popup_anchor=(0, -40),
    )

    folium.Marker(
        location=coords, popup=f"Author: {user.username}", icon=custom_icon
    ).add_to(m)
    return m._repr_html_()
