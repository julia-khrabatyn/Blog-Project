import nh3

from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User
from .services import get_coordinates

__all__ = [
    "handle_user_pre_save",
]


def _clean_user_bio(instance):
    """Private function for cleaning user's bio with nh3 for safety reasons."""
    if instance.bio:
        instance.bio = nh3.clean(instance.bio, **settings.NH3_BIO_SETTINGS)


def _handle_geocoding(instance):
    """Private function for updating user's coordinates if geodata provided."""
    changed = False

    if not instance.pk:
        changed = True

    else:
        try:
            old_instance = User.objects.only("city", "country").get(
                pk=instance.pk
            )
            changed = (
                old_instance.city != instance.city
                or old_instance.country != instance.country
            )
        except User.DoesNotExist:
            changed = True

    if changed:
        if instance.city or instance.country:
            country_code = str(instance.country) if instance.country else None
            coords = get_coordinates(instance.city, country_code)
            if coords:
                instance.latitude, instance.longitude = coords
            else:
                instance.latitude = instance.longitude = None
        else:
            instance.latitude = instance.longitude = None


@receiver(
    pre_save, sender=User, dispatch_uid="accounts.signals.handle_user_pre_save"
)
def handle_user_pre_save(sender, instance, **kwargs):
    """Main function for handling pre_save."""
    _clean_user_bio(instance)
    _handle_geocoding(instance)
