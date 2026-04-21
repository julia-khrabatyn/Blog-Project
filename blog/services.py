import folium
import random

from constance import config
from folium.plugins import HeatMap

__all__ = ["generate_users_heatmap"]


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
