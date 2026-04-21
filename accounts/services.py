import logging

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from constance import config

__all__ = ["get_coordinates"]

logger = logging.getLogger("accounts")


def get_coordinates(city: str = None, country_code: str = None):
    """
    Function for returning coordinates from user's country (city) if provided by user.
    Country - 2-letter country code, for instance: Ukraine -> UA
    City - city name.
    """
    if not city and not country_code:
        return None

    if city:
        query = city
        feature_type = "city"

    else:
        query = country_code
        feature_type = None

    geolocator = Nominatim(user_agent="byline_blog_app")

    try:
        location = geolocator.geocode(
            query,
            exactly_one=True,
            country_codes=country_code,
            featuretype=feature_type,
        )

        if location:
            return [location.latitude, location.longitude]

    except GeocoderTimedOut:
        logger.error("Geocoder Timeout error was occurred!")

    except Exception as e:
        logger.error(f"Geopy error: {e} was occurred!", exc_info=True)

    return None
