import logging

from django.conf import settings
from django.dispatch import receiver

from pathlib import Path

from constance.signals import config_updated

logger = logging.getLogger("__name__")

__all__ = [
    "cleanup_old_default_avatar",
]


@receiver(config_updated)
def cleanup_old_default_avatar(sender, key, old_value, new_value, **kwargs):
    """Signal to get rid of old default avatar image (for deleting garbage files in media root)."""
    if key == "DEFAULT_AVATAR":
        old_value_str = str(old_value) if old_value else ""
        new_value_str = str(new_value) if new_value else ""

        if (
            old_value_str
            and not old_value_str.startswith("images/")
            and old_value_str != new_value_str
        ):
            old_file_path = Path(settings.MEDIA_ROOT) / old_value_str
            if old_file_path.is_file():
                try:
                    old_file_path.unlink()
                    logger.info(
                        f"Successfully delete old default avatar {old_value_str}"
                    )
                except OSError:
                    logger.error(
                        f"OSError was occured while deleting {old_value_str}",
                        exc_info=True,
                    )
                except Exception as e:
                    logger.error(
                        f"Error: {e} was occured while deleting {old_value_str}",
                        exc_info=True,
                    )
